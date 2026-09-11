import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import org.deidentifier.arx.ARXAnonymizer;
import org.deidentifier.arx.ARXConfiguration;
import org.deidentifier.arx.ARXLattice;
import org.deidentifier.arx.ARXLattice.ARXNode;
import org.deidentifier.arx.ARXResult;
import org.deidentifier.arx.AttributeType;
import org.deidentifier.arx.AttributeType.Hierarchy;
import org.deidentifier.arx.Data;
import org.deidentifier.arx.DataHandle;
import org.deidentifier.arx.criteria.DistinctLDiversity;
import org.deidentifier.arx.criteria.EqualDistanceTCloseness;
import org.deidentifier.arx.criteria.KAnonymity;
import org.deidentifier.arx.metric.Metric;
import org.deidentifier.arx.risk.RiskModelSampleRisks;

public class CompareTransformations {

    private static final String BASE =
        System.getProperty("user.home") + "/arx_project";

    private static Data buildData() throws Exception {

        Data data = Data.create(
            BASE + "/data/patients.csv",
            StandardCharsets.UTF_8,
            ','
        );

        data.getDefinition().setAttributeType(
            "zipcode",
            Hierarchy.create(
                BASE + "/hierarchies/zipcode_hierarchy.csv",
                StandardCharsets.UTF_8,
                ','
            )
        );

        data.getDefinition().setAttributeType(
            "age",
            Hierarchy.create(
                BASE + "/hierarchies/age_hierarchy.csv",
                StandardCharsets.UTF_8,
                ','
            )
        );

        data.getDefinition().setAttributeType(
            "gender",
            Hierarchy.create(
                BASE + "/hierarchies/gender_hierarchy.csv",
                StandardCharsets.UTF_8,
                ','
            )
        );

        data.getDefinition().setAttributeType(
            "nationality",
            Hierarchy.create(
                BASE + "/hierarchies/nationality_hierarchy.csv",
                StandardCharsets.UTF_8,
                ','
            )
        );

        data.getDefinition().setAttributeType(
            "admission_date",
            Hierarchy.create(
                BASE + "/hierarchies/admission_date_hierarchy.csv",
                StandardCharsets.UTF_8,
                ','
            )
        );

        data.getDefinition().setAttributeType(
            "diagnosis",
            AttributeType.SENSITIVE_ATTRIBUTE
        );

        return data;
    }

    private static ARXConfiguration buildConfig() {

        ARXConfiguration config =
            ARXConfiguration.create();

        config.addPrivacyModel(
            new KAnonymity(5)
        );

        config.addPrivacyModel(
            new DistinctLDiversity(
                "diagnosis",
                3
            )
        );

        config.addPrivacyModel(
            new EqualDistanceTCloseness(
                "diagnosis",
                0.2d
            )
        );

        config.setSuppressionLimit(0.05d);

        config.setQualityModel(
            Metric.createLossMetric()
        );

        return config;
    }

    private static String describe(
        String label,
        ARXNode node,
        DataHandle handle
    ) {

        RiskModelSampleRisks risks =
            handle
                .getRiskEstimator()
                .getSampleBasedReidentificationRisk();

        long suppressed = 0;

        for (
            int row = 0;
            row < handle.getNumRows();
            row++
        ) {
            if (handle.isOutlier(row)) {
                suppressed++;
            }
        }

        double suppression =
            handle.getNumRows() == 0
            ? 0d
            : (
                (double) suppressed /
                (double) handle.getNumRows()
            ) * 100d;

        StringBuilder text =
            new StringBuilder();

        text.append(label).append("\n");
        text.append(
            "transformation = "
        ).append(
            Arrays.toString(
                node.getTransformation()
            )
        ).append("\n");

        text.append(
            "total generalization level = "
        ).append(
            node.getTotalGeneralizationLevel()
        ).append("\n");

        text.append(
            "lowest loss score = "
        ).append(
            node.getLowestScore()
        ).append("\n");

        text.append(
            "highest loss score = "
        ).append(
            node.getHighestScore()
        ).append("\n");

        text.append(
            "suppression rate = "
        ).append(
            suppression
        ).append("%\n");

        text.append(
            "highest sample risk = "
        ).append(
            risks.getHighestRisk() * 100d
        ).append("%\n");

        text.append(
            "prosecutor risk = "
        ).append(
            risks.getEstimatedProsecutorRisk()
            * 100d
        ).append("%\n");

        text.append(
            "journalist risk = "
        ).append(
            risks.getEstimatedJournalistRisk()
            * 100d
        ).append("%\n");

        text.append(
            "marketer risk = "
        ).append(
            risks.getEstimatedMarketerRisk()
            * 100d
        ).append("%\n");

        return text.toString();
    }

    public static void main(
        String[] args
    ) throws Exception {

        Data data = buildData();

        ARXResult result =
            new ARXAnonymizer().anonymize(
                data,
                buildConfig()
            );

        if (!result.isResultAvailable()) {
            throw new IllegalStateException(
                "No valid ARX solution"
            );
        }

        ARXNode optimum =
            result.getGlobalOptimum();

        ARXLattice lattice =
            result.getLattice();

        lattice.expand(optimum);

        ARXNode comparison = null;

        if (
            optimum.getSuccessors() != null &&
            optimum.getSuccessors().length > 0
        ) {
            comparison =
                optimum.getSuccessors()[0];
        } else if (
            optimum.getPredecessors() != null &&
            optimum.getPredecessors().length > 0
        ) {
            comparison =
                optimum.getPredecessors()[0];
        }

        if (comparison == null) {
            throw new IllegalStateException(
                "No comparison node available"
            );
        }

        DataHandle optimumHandle =
            result.getOutput(
                optimum,
                true
            );

        DataHandle comparisonHandle =
            result.getOutput(
                comparison,
                true
            );

        StringBuilder report =
            new StringBuilder();

        report.append(
            "Transformation comparison\n"
        );

        report.append(
            "=========================\n\n"
        );

        report.append(
            describe(
                "OPTIMAL NODE",
                optimum,
                optimumHandle
            )
        );

        report.append("\n");

        report.append(
            describe(
                "COMPARISON NODE",
                comparison,
                comparisonHandle
            )
        );

        report.append("\n");

        report.append(
            "Interpretation\n"
        );

        report.append(
            "--------------\n"
        );

        report.append(
            "Lower ARX loss scores indicate "
            + "better retained utility.\n"
        );

        report.append(
            "The global optimum is ARX's "
            + "selected minimum-loss solution "
            + "under the configured constraints.\n"
        );

        java.nio.file.Files.writeString(
            new File(
                BASE +
                "/evidence/transformation_comparison.txt"
            ).toPath(),
            report.toString(),
            StandardCharsets.UTF_8
        );

        System.out.println(report);
    }
}
