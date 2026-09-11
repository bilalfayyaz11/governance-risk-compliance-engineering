import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import org.deidentifier.arx.ARXAnonymizer;
import org.deidentifier.arx.ARXConfiguration;
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

public class HealthcareAnonymizer {

    private static final String BASE =
        System.getProperty("user.home") + "/arx_project";

    public static void main(String[] args) throws Exception {

        String input =
            BASE + "/data/patients.csv";

        String output =
            BASE + "/output/patients_anonymized.csv";

        String metrics =
            BASE + "/evidence/anonymization_metrics.txt";

        Data data = Data.create(
            input,
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

        ARXAnonymizer anonymizer =
            new ARXAnonymizer();

        ARXResult result =
            anonymizer.anonymize(
                data,
                config
            );

        if (!result.isResultAvailable()) {
            throw new IllegalStateException(
                "No privacy-preserving solution found"
            );
        }

        ARXNode optimum =
            result.getGlobalOptimum();

        DataHandle handle =
            result.getOutput(false);

        handle.save(output, ',');

        RiskModelSampleRisks risks =
            handle
                .getRiskEstimator()
                .getSampleBasedReidentificationRisk();

        long suppressed = 0;

        for (int row = 0;
             row < handle.getNumRows();
             row++) {

            if (handle.isOutlier(row)) {
                suppressed++;
            }
        }

        double suppressionRate =
            handle.getNumRows() == 0
            ? 0d
            : ((double) suppressed /
               (double) handle.getNumRows());

        String[] qis =
            optimum.getQuasiIdentifyingAttributes();

        StringBuilder report =
            new StringBuilder();

        report.append(
            "ARX anonymization result\n"
        );

        report.append(
            "========================\n"
        );

        report.append(
            "k = 5\n"
        );

        report.append(
            "distinct l = 3\n"
        );

        report.append(
            "t = 0.2\n"
        );

        report.append(
            "t-closeness distance = "
            + "equal-distance EMD\n"
        );

        report.append(
            "suppression limit = 5%\n"
        );

        report.append(
            "records = "
            + handle.getNumRows()
            + "\n"
        );

        report.append(
            "suppressed records = "
            + suppressed
            + "\n"
        );

        report.append(
            "suppression rate = "
            + (suppressionRate * 100d)
            + "%\n"
        );

        report.append(
            "optimum found = "
            + result.getOptimumFound()
            + "\n"
        );

        report.append(
            "runtime ms = "
            + result.getTime()
            + "\n"
        );

        report.append(
            "QI attributes = "
            + Arrays.toString(qis)
            + "\n"
        );

        report.append(
            "transformation = "
            + Arrays.toString(
                optimum.getTransformation()
            )
            + "\n"
        );

        report.append(
            "total generalization level = "
            + optimum.getTotalGeneralizationLevel()
            + "\n"
        );

        report.append(
            "lowest information-loss score = "
            + optimum.getLowestScore()
            + "\n"
        );

        report.append(
            "highest information-loss score = "
            + optimum.getHighestScore()
            + "\n"
        );

        report.append(
            "highest sample risk = "
            + (risks.getHighestRisk() * 100d)
            + "%\n"
        );

        report.append(
            "average sample risk = "
            + (risks.getAverageRisk() * 100d)
            + "%\n"
        );

        report.append(
            "prosecutor risk = "
            + (
                risks.getEstimatedProsecutorRisk()
                * 100d
            )
            + "%\n"
        );

        report.append(
            "journalist risk = "
            + (
                risks.getEstimatedJournalistRisk()
                * 100d
            )
            + "%\n"
        );

        report.append(
            "marketer risk = "
            + (
                risks.getEstimatedMarketerRisk()
                * 100d
            )
            + "%\n"
        );

        java.nio.file.Files.writeString(
            new File(metrics).toPath(),
            report.toString(),
            StandardCharsets.UTF_8
        );

        System.out.println(report);

        System.out.println(
            "Output: " + output
        );

        System.out.println(
            "Metrics: " + metrics
        );
    }
}
