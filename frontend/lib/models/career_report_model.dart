class CareerReport {
  final String studentName;
  final String top1Cluster;
  final String top2Cluster;
  final String top3Cluster;
  final List<String> roles;
  final int salaryMin;
  final int salaryMax;
  final int salaryMid;
  final int futureSalaryMin;
  final int futureSalaryMax;
  final int futureSalaryMid;
  final double writingClarity;
  final double writingStructure;
  final double writingConfidence;
  final double writingAnalytical;
  final double writingCreativity;
  final double overallWritingScore;
  final String demandTrend;
  final List<dynamic> educationPrograms;
  final List<dynamic> vacancyMatches;
  final String finalRole;
  final String confidenceLabel;
  final double finalScore;
  final String finalExplanation;
  final Map<String, dynamic> clusterData;
  final String interestCode;
  final Map<String, double> riasec;
  final Map<String, double> topComposites;

  CareerReport({
    this.studentName = 'Student',
    required this.top1Cluster,
    required this.top2Cluster,
    required this.top3Cluster,
    required this.roles,
    required this.salaryMin,
    required this.salaryMax,
    this.salaryMid = 0,
    this.futureSalaryMin = 0,
    this.futureSalaryMax = 0,
    this.futureSalaryMid = 0,
    required this.writingClarity,
    required this.writingStructure,
    required this.writingConfidence,
    required this.writingAnalytical,
    required this.writingCreativity,
    required this.overallWritingScore,
    required this.demandTrend,
    required this.educationPrograms,
    required this.vacancyMatches,
    required this.finalRole,
    required this.confidenceLabel,
    required this.finalScore,
    required this.finalExplanation,
    this.clusterData = const {},
    this.interestCode = '',
    this.riasec = const {},
    this.topComposites = const {},
  });

  factory CareerReport.fromJson(Map<String, dynamic> j) {
    Map<String, double> riasecMap = {};
    final rawRiasec = j['riasec'];
    if (rawRiasec is Map) {
      rawRiasec.forEach((k, v) {
        riasecMap[k.toString()] = (v ?? 50).toDouble();
      });
    }

    const compositeKeys = [
      'Analytical_Thinking','Data_Literacy','Technical_ProblemSolving',
      'Tech_Adaptability','Process_Optimization','Career_Growth_Mindset',
      'Future_Orientation','Innovation_Drive','Leadership_Capability',
      'Creativity_Index','Social_Intelligence','Communication_Skill',
    ];

    Map<String, double> compositesMap = {};
    final rawFeatures = j['features'] ?? {};
    if (rawFeatures is Map) {
      for (final key in compositeKeys) {
        final val = rawFeatures[key];
        if (val != null) {
          compositesMap[key] = ((val as num).toDouble() * 100).clamp(0, 100);
        }
      }
    }

    return CareerReport(
      studentName:        j['student_name'] ?? 'Student',
      top1Cluster:        j['top1_cluster'] ?? '',
      top2Cluster:        j['top2_cluster'] ?? '',
      top3Cluster:        j['top3_cluster'] ?? '',
      roles:              List<String>.from(j['recommended_roles'] ?? []),
      salaryMin:          (j['salary_min'] ?? 0).toInt(),
      salaryMax:          (j['salary_max'] ?? 0).toInt(),
      salaryMid:          (j['salary_mid'] ?? 0).toInt(),
      futureSalaryMin:    (j['future_salary_min'] ?? 0).toInt(),
      futureSalaryMax:    (j['future_salary_max'] ?? 0).toInt(),
      futureSalaryMid:    (j['future_salary_mid'] ?? 0).toInt(),
      writingClarity:     (j['writing_clarity'] ?? 50).toDouble(),
      writingStructure:   (j['writing_structure'] ?? 50).toDouble(),
      writingConfidence:  (j['writing_confidence'] ?? 50).toDouble(),
      writingAnalytical:  (j['writing_analytical'] ?? 50).toDouble(),
      writingCreativity:  (j['writing_creativity'] ?? 50).toDouble(),
      overallWritingScore:(j['overall_writing_score'] ?? 50).toDouble(),
      demandTrend:        j['demand_trend'] ?? 'Stable',
      educationPrograms:  List<dynamic>.from(j['education_programs'] ?? []),
      vacancyMatches:     List<dynamic>.from(j['vacancy_matches'] ?? []),
      finalRole:          j['final_recommended_role'] ?? '',
      confidenceLabel:    j['confidence_label'] ?? 'Medium',
      finalScore:         (j['final_score'] ?? 0).toDouble(),
      finalExplanation:   j['final_explanation'] ?? '',
      clusterData:        Map<String, dynamic>.from(j['cluster_data'] ?? {}),
      interestCode:       j['interest_code'] ?? '',
      riasec:             riasecMap,
      topComposites:      compositesMap,
    );
  }
}
