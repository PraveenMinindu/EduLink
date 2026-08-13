import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';

class CompareScreen extends StatefulWidget {
  final CareerReport report;
  const CompareScreen({super.key, required this.report});
  @override
  State<CompareScreen> createState() => _CompareScreenState();
}

class _CompareScreenState extends State<CompareScreen> {
  int _selA = 0;
  int _selB = 1;

  List<String> get _clusterKeys => [
        widget.report.top1Cluster,
        widget.report.top2Cluster,
        widget.report.top3Cluster,
      ];

  List<String> get _clusterNames =>
      _clusterKeys.map((c) => c.replaceAll('_', ' ')).toList();

  Map<String, dynamic> _dataFor(int selIndex) {
    final key  = _clusterKeys[selIndex];
    final data = widget.report.clusterData[key];
    if (data != null) return Map<String, dynamic>.from(data);
    return {
      "role":         selIndex == 0 ? widget.report.finalRole : "Role",
      "salary_min":   selIndex == 0 ? widget.report.salaryMin : 0,
      "salary_max":   selIndex == 0 ? widget.report.salaryMax : 0,
      "salary_mid":   selIndex == 0 ? widget.report.salaryMid : 0,
      "demand_trend": selIndex == 0 ? widget.report.demandTrend : "Stable",
      "demand_score": selIndex == 0 ? 80 : 50,
      "fit_score":    selIndex == 0
          ? widget.report.finalScore
          : widget.report.finalScore * 0.75,
      "edu_level": "Degree",
    };
  }

  String _fmt(dynamic n) {
    final val = n == null ? 0 : (n is int ? n : (n as double).toInt());
    if (val == 0) return "N/A";
    if (val >= 1000) return "LKR ${(val / 1000).toStringAsFixed(0)}K";
    return "LKR $val";
  }

  String _demandLabel(dynamic score) {
    final s = score == null
        ? 50.0
        : (score is int ? score.toDouble() : score as double);
    if (s >= 70) return "High";
    if (s >= 40) return "Moderate";
    return "Low";
  }

  int _winner(dynamic a, dynamic b, bool higherIsBetter) {
    final av = a == null ? 0.0 : (a is int ? a.toDouble() : a as double);
    final bv = b == null ? 0.0 : (b is int ? b.toDouble() : b as double);
    if (av == bv) return -1;
    return higherIsBetter ? (av > bv ? 0 : 1) : (av < bv ? 0 : 1);
  }

  List<Map<String, dynamic>> _buildMetrics(
    Map<String, dynamic> dA,
    Map<String, dynamic> dB,
  ) {
    return [
      {
        "label":  "Role",
        "dispA":  dA["role"] ?? "Unknown",
        "dispB":  dB["role"] ?? "Unknown",
        "winner": -1,
      },
      {
        "label":  "Avg Salary",
        "dispA":  _fmt(dA["salary_mid"]),
        "dispB":  _fmt(dB["salary_mid"]),
        "winner": _winner(dA["salary_mid"], dB["salary_mid"], true),
      },
      {
        "label":  "Salary Range",
        "dispA":  "${_fmt(dA["salary_min"])} – ${_fmt(dA["salary_max"])}",
        "dispB":  "${_fmt(dB["salary_min"])} – ${_fmt(dB["salary_max"])}",
        "winner": _winner(dA["salary_mid"], dB["salary_mid"], true),
      },
      {
        "label":  "Demand Trend",
        "dispA":  dA["demand_trend"] ?? "Stable",
        "dispB":  dB["demand_trend"] ?? "Stable",
        "winner": _winner(dA["demand_score"], dB["demand_score"], true),
      },
      {
        "label":  "Job Openings",
        "dispA":  _demandLabel(dA["demand_score"]),
        "dispB":  _demandLabel(dB["demand_score"]),
        "winner": _winner(dA["demand_score"], dB["demand_score"], true),
      },
      {
        "label":  "Education",
        "dispA":  dA["edu_level"] ?? "Degree",
        "dispB":  dB["edu_level"] ?? "Degree",
        "winner": -1,
      },
      {
        "label":  "Profile Fit",
        "dispA":  "${_fitInt(dA["fit_score"])}%",
        "dispB":  "${_fitInt(dB["fit_score"])}%",
        "winner": _winner(dA["fit_score"], dB["fit_score"], true),
      },
    ];
  }

  int _fitInt(dynamic v) {
    if (v == null) return 0;
    return (v is int ? v.toDouble() : v as double).toInt();
  }

  double _fitVal(dynamic v) {
    if (v == null) return 0.0;
    final d = v is int ? v.toDouble() : v as double;
    return (d / 100).clamp(0.0, 1.0);
  }

  @override
  Widget build(BuildContext context) {
    final dA      = _dataFor(_selA);
    final dB      = _dataFor(_selB);
    final metrics = _buildMetrics(dA, dB);

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 54, 22, 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GestureDetector(
                  onTap: () => Navigator.pop(context),
                  child: Row(children: [
                    const Icon(Icons.arrow_back_ios,
                        color: Colors.white54, size: 16),
                    const Text("Report",
                        style: TextStyle(
                            color: Colors.white54, fontSize: 13)),
                  ]),
                ),
                const SizedBox(height: 12),
                Text("Compare careers",
                    style: GoogleFonts.playfairDisplay(
                        fontSize: 26,
                        color: Colors.white,
                        fontWeight: FontWeight.w700)),
                Text("Select two clusters to compare side by side",
                    style: TextStyle(
                        fontSize: 12,
                        color: Colors.white.withOpacity(0.5))),
              ],
            ),
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [

                  _sectionLabel("SELECT CLUSTER A", AppColors.blue),
                  const SizedBox(height: 8),
                  _clusterRow(_selA, AppColors.blue, AppColors.bluePale,
                      (i) => setState(() => _selA = i)),
                  const SizedBox(height: 14),

                  _sectionLabel("SELECT CLUSTER B", AppColors.violet),
                  const SizedBox(height: 8),
                  _clusterRow(_selB, AppColors.violet,
                      AppColors.violetPale,
                      (i) => setState(() => _selB = i)),
                  const SizedBox(height: 12),

                  // Real data badge
                  if (widget.report.clusterData.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: AppColors.mintPale,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                            color:
                                AppColors.mint.withOpacity(0.3)),
                      ),
                      child: Row(children: [
                        const Icon(Icons.verified_outlined,
                            color: AppColors.mint, size: 14),
                        const SizedBox(width: 6),
                        const Expanded(
                          child: Text(
                            "Real data — salary model + demand forecasting per cluster",
                            style: TextStyle(
                                fontSize: 11,
                                color: AppColors.mint,
                                fontWeight: FontWeight.w500),
                          ),
                        ),
                      ]),
                    ),
                  const SizedBox(height: 12),

                  // Comparison table
                  Container(
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(children: [
                      // Header
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 12),
                        decoration: const BoxDecoration(
                          color: AppColors.navy,
                          borderRadius: BorderRadius.vertical(
                              top: Radius.circular(16)),
                        ),
                        child: Row(children: [
                          const Expanded(
                            flex: 2,
                            child: Text("Metric",
                                style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w700,
                                    color: Colors.white)),
                          ),
                          Expanded(
                            child: Text(
                              _clusterNames[_selA],
                              style: const TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w700,
                                  color: Color(0xFF60A5FA)),
                              textAlign: TextAlign.center,
                            ),
                          ),
                          Expanded(
                            child: Text(
                              _clusterNames[_selB],
                              style: const TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w700,
                                  color: Color(0xFFA78BFA)),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ]),
                      ),

                      // Rows — real data changes per selection
                      ...metrics.asMap().entries.map((e) {
                        final i      = e.key;
                        final m      = e.value;
                        final isLast = i == metrics.length - 1;
                        final winner = m["winner"] as int;

                        return Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 12, vertical: 11),
                          decoration: BoxDecoration(
                            color: i % 2 == 0
                                ? AppColors.surface
                                : AppColors.card,
                            borderRadius: isLast
                                ? const BorderRadius.vertical(
                                    bottom: Radius.circular(16))
                                : BorderRadius.zero,
                          ),
                          child: Row(children: [
                            Expanded(
                              flex: 2,
                              child: Text(m["label"],
                                  style: const TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                      color: AppColors.text2)),
                            ),
                            Expanded(
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.center,
                                children: [
                                  if (winner == 0)
                                    const Icon(Icons.star,
                                        color: AppColors.mint,
                                        size: 10),
                                  const SizedBox(width: 2),
                                  Flexible(
                                    child: Text(
                                      m["dispA"],
                                      style: TextStyle(
                                        fontSize: 11,
                                        fontWeight: winner == 0
                                            ? FontWeight.w700
                                            : FontWeight.w400,
                                        color: winner == 0
                                            ? AppColors.blue
                                            : AppColors.text2,
                                      ),
                                      textAlign: TextAlign.center,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Expanded(
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.center,
                                children: [
                                  if (winner == 1)
                                    const Icon(Icons.star,
                                        color: AppColors.mint,
                                        size: 10),
                                  const SizedBox(width: 2),
                                  Flexible(
                                    child: Text(
                                      m["dispB"],
                                      style: TextStyle(
                                        fontSize: 11,
                                        fontWeight: winner == 1
                                            ? FontWeight.w700
                                            : FontWeight.w400,
                                        color: winner == 1
                                            ? AppColors.violet
                                            : AppColors.text2,
                                      ),
                                      textAlign: TextAlign.center,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ]),
                        );
                      }),
                    ]),
                  ),
                  const SizedBox(height: 16),

                  // Fit bars
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _sectionLabel(
                              "YOUR PROFILE FIT", AppColors.text3),
                          const SizedBox(height: 12),
                          _fitBar(_clusterNames[_selA],
                              _fitVal(dA["fit_score"]), AppColors.blue),
                          const SizedBox(height: 10),
                          _fitBar(_clusterNames[_selB],
                              _fitVal(dB["fit_score"]),
                              AppColors.violet),
                          const SizedBox(height: 8),
                          const Text(
                            "Calculated from your MCQ responses using the career fit model",
                            style: TextStyle(
                                fontSize: 10, color: AppColors.text3),
                          ),
                        ]),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _clusterRow(
    int selected,
    Color color,
    Color paleBg,
    Function(int) onTap,
  ) =>
      Row(
        children: List.generate(
          _clusterNames.length,
          (i) => Expanded(
            child: GestureDetector(
              onTap: () => onTap(i),
              child: Container(
                margin: EdgeInsets.only(
                    right: i < _clusterNames.length - 1 ? 6 : 0),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: selected == i ? paleBg : AppColors.card,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: selected == i ? color : AppColors.border,
                    width: selected == i ? 1.5 : 1,
                  ),
                ),
                child: Text(
                  _clusterNames[i],
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: selected == i ? color : AppColors.text2,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ),
        ),
      );

  Widget _sectionLabel(String text, Color color) => Text(
        text,
        style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w700,
            color: color,
            letterSpacing: 0.5),
      );

  Widget _fitBar(String label, double val, Color color) =>
      Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(label,
                    style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: color),
                    overflow: TextOverflow.ellipsis),
              ),
              Text("${(val * 100).toInt()}% match",
                  style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: AppColors.navy)),
            ]),
        const SizedBox(height: 5),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: val,
            minHeight: 8,
            backgroundColor: AppColors.surface,
            valueColor: AlwaysStoppedAnimation(color),
          ),
        ),
      ]);
}
