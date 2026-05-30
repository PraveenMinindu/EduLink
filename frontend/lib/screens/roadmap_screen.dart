import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';

class RoadmapScreen extends StatelessWidget {
  final CareerReport report;
  const RoadmapScreen({super.key, required this.report});

  String _fmt(int n) =>
      n >= 1000 ? "LKR ${(n / 1000).toStringAsFixed(0)}K" : "LKR $n";

  @override
  Widget build(BuildContext context) {
    final role    = report.finalRole;
    final cluster = report.top1Cluster.replaceAll('_', ' ');

    // Build strengths from real writing scores
    final strengths = <Map<String, dynamic>>[];
    final toImprove = <Map<String, dynamic>>[];

    if (report.writingAnalytical >= 65)
      strengths.add(_skill(AppColors.mint, "Analytical thinking"));
    if (report.writingClarity >= 65)
      strengths.add(_skill(AppColors.mint, "Clear communication"));
    if (report.writingConfidence >= 65)
      strengths.add(_skill(AppColors.mint, "Confidence"));
    if (report.writingCreativity >= 65)
      strengths.add(_skill(AppColors.mint, "Creativity"));
    if (strengths.isEmpty)
      strengths.add(_skill(AppColors.mint, "Completing full assessment"));

    if (report.writingAnalytical < 65)
      toImprove.add(_skill(AppColors.rose, "Analytical writing"));
    if (report.writingCreativity < 65)
      toImprove.add(_skill(AppColors.gold, "Creative thinking"));
    if (report.writingConfidence < 65)
      toImprove.add(_skill(AppColors.gold, "Writing confidence"));

    // Education institute from real data
    final eduInstitute = report.educationPrograms.isNotEmpty
        ? report.educationPrograms[0]['institute'] ?? "a recommended institute"
        : "a recommended institute";

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // Header
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
                Text("Career roadmap",
                    style: GoogleFonts.playfairDisplay(
                        fontSize: 26,
                        color: Colors.white,
                        fontWeight: FontWeight.w700)),
                Text("Your 3-phase journey to $role",
                    style: TextStyle(
                        fontSize: 12,
                        color: Colors.white.withOpacity(0.5))),
              ],
            ),
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(children: [

                // Phase 1 — Now
                _phase(
                  dot: "N",
                  dotColor: AppColors.navy,
                  label: "NOW — Where you are",
                  labelColor: AppColors.navy,
                  title: "Current profile",
                  items: [
                    _item(AppColors.text3, "A/L Technology student"),
                    ...strengths.map((s) =>
                      _item(AppColors.mint, s["text"] as String)),
                    ...toImprove.map((w) =>
                      _item(AppColors.rose,
                          "Needs improvement: ${w["text"]}")),
                  ],
                  skills: strengths.isEmpty
                      ? [_skill(AppColors.mint, "Assessment completed")]
                      : strengths.take(4).toList(),
                  showLine: true,
                ),

                // Phase 2 — 6 months
                _phase(
                  dot: "6M",
                  dotColor: AppColors.blue,
                  label: "6 MONTHS — Education & skills",
                  labelColor: AppColors.blue,
                  title: "Education and skill building",
                  items: [
                    _item(AppColors.blue, "Enrol at $eduInstitute"),
                    _item(AppColors.blue,
                        "Build foundation skills for $cluster"),
                    _item(AppColors.blue,
                        "Complete your first portfolio project"),
                    _item(AppColors.blue,
                        "Improve writing score (now ${report.overallWritingScore.toInt()}/100)"),
                  ],
                  skills: [
                    _skill(AppColors.blue, "Technical foundations"),
                    _skill(AppColors.blue, "Portfolio project"),
                    _skill(AppColors.blue, "Writing improvement"),
                    _skill(AppColors.blue, "Online courses"),
                  ],
                  showLine: true,
                ),

                // Phase 3 — 2 years
                _phase(
                  dot: "2Y",
                  dotColor: AppColors.mint,
                  label: "2 YEARS — Target role",
                  labelColor: AppColors.mint,
                  title: "$role — Entry level",
                  items: [
                    _item(AppColors.mint,
                        "Apply for internships in $cluster"),
                    _item(AppColors.mint,
                        "Build portfolio of 3+ real projects"),
                    _item(AppColors.mint,
                        "Salary target: ${_fmt(report.salaryMin)} – ${_fmt(report.salaryMax)} / month"),
                    _item(AppColors.mint,
                        "Market demand: ${report.demandTrend} in Sri Lanka"),
                  ],
                  skills: [
                    _skill(AppColors.mint, role),
                    _skill(AppColors.mint, cluster),
                    _skill(AppColors.mint, "Sri Lanka IT market"),
                    _skill(AppColors.mint, "Portfolio ready"),
                  ],
                  showLine: false,
                ),

              ]),
            ),
          ),
        ],
      ),
    );
  }

  Map<String, dynamic> _item(Color color, String text) =>
      {"color": color, "text": text};

  Map<String, dynamic> _skill(Color color, String text) =>
      {"color": color, "text": text};

  Widget _phase({
    required String dot,
    required Color dotColor,
    required String label,
    required Color labelColor,
    required String title,
    required List<Map<String, dynamic>> items,
    required List<Map<String, dynamic>> skills,
    required bool showLine,
  }) =>
      IntrinsicHeight(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Column(children: [
              Container(
                width: 36,
                height: 36,
                decoration:
                    BoxDecoration(color: dotColor, shape: BoxShape.circle),
                child: Center(
                  child: Text(dot,
                      style: const TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w700,
                          color: Colors.white)),
                ),
              ),
              if (showLine)
                Expanded(
                  child: Container(
                      width: 2,
                      color: AppColors.border,
                      margin: const EdgeInsets.only(top: 4)),
                ),
            ]),
            const SizedBox(width: 14),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.only(bottom: 24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(label,
                        style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: labelColor,
                            letterSpacing: 0.4)),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.card,
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(title,
                              style: const TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.text1)),
                          const SizedBox(height: 10),
                          ...items.map((item) => Padding(
                                padding: const EdgeInsets.only(bottom: 7),
                                child: Row(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                  children: [
                                    Container(
                                      width: 6,
                                      height: 6,
                                      margin: const EdgeInsets.only(
                                          top: 5, right: 8),
                                      decoration: BoxDecoration(
                                          color: item["color"],
                                          shape: BoxShape.circle),
                                    ),
                                    Expanded(
                                      child: Text(item["text"],
                                          style: const TextStyle(
                                              fontSize: 12,
                                              color: AppColors.text2,
                                              height: 1.4)),
                                    ),
                                  ],
                                ),
                              )),
                          const SizedBox(height: 8),
                          Wrap(
                            spacing: 6,
                            runSpacing: 6,
                            children: skills
                                .map((s) => Container(
                                      padding:
                                          const EdgeInsets.symmetric(
                                              horizontal: 10, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: (s["color"] as Color)
                                            .withOpacity(0.1),
                                        borderRadius:
                                            BorderRadius.circular(20),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Container(
                                              width: 5,
                                              height: 5,
                                              decoration: BoxDecoration(
                                                  color: s["color"],
                                                  shape: BoxShape.circle)),
                                          const SizedBox(width: 5),
                                          Text(s["text"],
                                              style: TextStyle(
                                                  fontSize: 10,
                                                  fontWeight:
                                                      FontWeight.w500,
                                                  color: s["color"])),
                                        ],
                                      ),
                                    ))
                                .toList(),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      );
}
