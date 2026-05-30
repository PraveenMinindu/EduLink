import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:fl_chart/fl_chart.dart';
//import 'package:url_launcher/url_launcher.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';
import '../../services/report_service.dart';
import 'roles_screen.dart';
import 'education_screen.dart';
import 'jobs_screen.dart';
import '../compare_screen.dart';
import '../roadmap_screen.dart';
import '../writing_tips_screen.dart';
import '../skill_gap_screen.dart';
import '../profile_screen.dart';
import 'package:share_plus/share_plus.dart';

class ReportScreen extends StatefulWidget {
  final String studentId;
  const ReportScreen({super.key, required this.studentId});
  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  CareerReport? _report;
  bool _loading = true;
  int _compositeTab = 0;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final r = await ReportService.getReport(widget.studentId);
    setState(() {
      _report = r;
      _loading = false;
    });
  }

  Color _confidenceColor(String label) {
    if (label == 'High') return AppColors.mint;
    if (label == 'Medium') return AppColors.gold;
    return AppColors.rose;
  }

  // ── Share helpers ─────────────────────────────────────────
  String get _shareText =>
      'I just completed my EduLink AI career assessment!\n\n'
      '🎯 Recommended Career: ${_report?.finalRole ?? ""}\n'
      '📊 Score: ${_report?.finalScore.toStringAsFixed(1) ?? ""} / 100\n'
      '🧠 Personality Code: ${_report?.interestCode ?? ""}\n\n'
      'Try EduLink for free: https://edulink.app';

  Future<void> _launchWhatsApp() async {
    await Share.share(_shareText);
  }

  Future<void> _launchEmail() async {
    await Share.share(_shareText, subject: 'My EduLink Career Report');
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        backgroundColor: AppColors.navy,
        body: Center(child: CircularProgressIndicator(color: Colors.white)),
      );
    }
    if (_report == null) {
      return const Scaffold(body: Center(child: Text("Report not found")));
    }
    final r = _report!;

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // ── Hero header ───────────────────────────────────
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 54, 22, 20),
            child: Column(
              children: [
                Row(
                  children: [
                    Container(
                      width: 44,
                      height: 44,
                      decoration: const BoxDecoration(
                        color: AppColors.blue,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(
                        Icons.person,
                        color: Colors.white,
                        size: 22,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            "Career Report",
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                          ),
                          Text(
                            widget.studentId,
                            style: TextStyle(
                              fontSize: 11,
                              color: Colors.white.withOpacity(0.5),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 5,
                      ),
                      decoration: BoxDecoration(
                        color: _confidenceColor(
                          r.confidenceLabel,
                        ).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        r.confidenceLabel,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: _confidenceColor(r.confidenceLabel),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.07),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.white.withOpacity(0.1)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "RECOMMENDED CAREER",
                        style: TextStyle(
                          fontSize: 10,
                          color: Colors.white.withOpacity(0.5),
                          fontWeight: FontWeight.w600,
                          letterSpacing: 0.5,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        r.finalRole,
                        style: GoogleFonts.playfairDisplay(
                          fontSize: 22,
                          color: Colors.white,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Score: ${r.finalScore.toStringAsFixed(1)} / 100",
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.white.withOpacity(0.6),
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 9,
                              vertical: 3,
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.mint.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              r.demandTrend,
                              style: const TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.w600,
                                color: AppColors.mint,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // ── Scrollable body ───────────────────────────────
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  // Career clusters
                  _sectionHeader("Career Clusters"),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Wrap(
                      spacing: 7,
                      runSpacing: 7,
                      children: [
                        _clusterChip(
                          r.top1Cluster,
                          AppColors.violetPale,
                          AppColors.violet,
                        ),
                        _clusterChip(
                          r.top2Cluster,
                          AppColors.bluePale,
                          AppColors.blue,
                        ),
                        _clusterChip(
                          r.top3Cluster,
                          AppColors.mintPale,
                          AppColors.mint,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Holland interest code
                  if (r.interestCode.isNotEmpty) ...[
                    _sectionHeader("Holland Interest Code"),
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.bluePale,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.blueMid),
                      ),
                      child: Row(
                        children: [
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  "Your personality code",
                                  style: TextStyle(
                                    fontSize: 10,
                                    color: AppColors.blue,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  r.interestCode.split('').join('  '),
                                  style: GoogleFonts.playfairDisplay(
                                    fontSize: 28,
                                    color: AppColors.navy,
                                    fontWeight: FontWeight.w700,
                                    letterSpacing: 4,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  _interestCodeLabel(r.interestCode),
                                  style: const TextStyle(
                                    fontSize: 10,
                                    color: AppColors.text2,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: [
                              const Text(
                                "Best career match",
                                style: TextStyle(
                                  fontSize: 10,
                                  color: AppColors.text3,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                r.finalRole,
                                style: const TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.blue,
                                ),
                              ),
                              Text(
                                r.top1Cluster.replaceAll('_', ' '),
                                style: const TextStyle(
                                  fontSize: 10,
                                  color: AppColors.text3,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],

                  // RIASEC radar
                  if (r.riasec.isNotEmpty) ...[
                    _sectionHeader("RIASEC Personality Radar"),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.card,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Column(
                        children: [
                          SizedBox(
                            height: 280,
                            child: _buildRadarChart(r.riasec),
                          ),
                          const SizedBox(height: 14),
                          Row(
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    _riasecLegend(
                                      'R',
                                      'Realistic',
                                      AppColors.riasecR,
                                      r.riasec['R'] ?? 0,
                                    ),
                                    const SizedBox(height: 6),
                                    _riasecLegend(
                                      'A',
                                      'Artistic',
                                      AppColors.riasecA,
                                      r.riasec['A'] ?? 0,
                                    ),
                                    const SizedBox(height: 6),
                                    _riasecLegend(
                                      'E',
                                      'Enterprising',
                                      AppColors.riasecE,
                                      r.riasec['E'] ?? 0,
                                    ),
                                  ],
                                ),
                              ),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    _riasecLegend(
                                      'I',
                                      'Investigative',
                                      AppColors.riasecI,
                                      r.riasec['I'] ?? 0,
                                    ),
                                    const SizedBox(height: 6),
                                    _riasecLegend(
                                      'S',
                                      'Social',
                                      AppColors.riasecS,
                                      r.riasec['S'] ?? 0,
                                    ),
                                    const SizedBox(height: 6),
                                    _riasecLegend(
                                      'C',
                                      'Conventional',
                                      AppColors.riasecC,
                                      r.riasec['C'] ?? 0,
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          _radarInterpretationWidget(r.riasec, r.finalRole),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],

                  // Top composites
                  if (r.topComposites.isNotEmpty) ...[
                    _sectionHeader("Top Psychological Strengths"),
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.card,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.border),
                      ),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              _compositeTabBtn('Technical', 0),
                              const SizedBox(width: 6),
                              _compositeTabBtn('Analytical', 1),
                              const SizedBox(width: 6),
                              _compositeTabBtn('Social', 2),
                            ],
                          ),
                          const SizedBox(height: 12),
                          ..._compositeRows(r.topComposites),
                          const SizedBox(height: 6),
                          const Text(
                            "Derived from your 40 MCQ answers using FEATURE_MAP",
                            style: TextStyle(
                              fontSize: 10,
                              color: AppColors.text3,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],

                  // Communication style
                  _sectionHeader(
                    "Communication Style",
                    action: "Get tips",
                    onAction: () => Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => WritingTipsScreen(report: r),
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      children: [
                        _scoreBar(
                          "Analytical",
                          r.writingAnalytical,
                          AppColors.blue,
                        ),
                        _scoreBar("Clarity", r.writingClarity, AppColors.blue),
                        _scoreBar(
                          "Confidence",
                          r.writingConfidence,
                          AppColors.violet,
                        ),
                        _scoreBar(
                          "Creativity",
                          r.writingCreativity,
                          AppColors.violet,
                        ),
                        _scoreBar(
                          "Structure",
                          r.writingStructure,
                          AppColors.mint,
                          last: true,
                        ),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: AppColors.surface,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text(
                            "Note: low writing score does not reduce your career prediction. MCQ scores carry 40% weight — writing carries 25%.",
                            style: TextStyle(
                              fontSize: 10,
                              color: AppColors.text3,
                              height: 1.4,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Salary estimate
                  _sectionHeader("Salary Estimate"),
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.border),
                    ),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: _statCard(
                                "Current (entry)",
                                "LKR ${_fmt(r.salaryMin)}–${_fmt(r.salaryMax)}",
                                "0–2 years",
                              ),
                            ),
                            const SizedBox(width: 10),
                            if (r.futureSalaryMid > 0)
                              Expanded(
                                child: _statCard(
                                  "Future (3–5 yrs)",
                                  "LKR ${_fmt(r.futureSalaryMin)}–${_fmt(r.futureSalaryMax)}",
                                  "mid level",
                                ),
                              ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 10,
                            vertical: 5,
                          ),
                          decoration: BoxDecoration(
                            color: AppColors.mintPale,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            "${r.demandTrend} market demand",
                            style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: AppColors.mint,
                            ),
                          ),
                        ),
                        const SizedBox(height: 6),
                        const Text(
                          "Source: PayScale Sri Lanka 2026  •  Glassdoor Colombo May 2026",
                          style: TextStyle(fontSize: 9, color: AppColors.text3),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Skill gap
                  _sectionHeader(
                    "Skill Gap",
                    action: "Full report",
                    onAction: () => Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => SkillGapScreen(
                          report: r,
                          studentId: widget.studentId,
                        ),
                      ),
                    ),
                  ),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.goldPale,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: AppColors.gold.withOpacity(0.3),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Areas for development",
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: AppColors.text1,
                          ),
                        ),
                        const SizedBox(height: 5),
                        Text(
                          r.writingCreativity < 65
                              ? "Creativity (${r.writingCreativity.toInt()}) and Confidence "
                                    "(${r.writingConfidence.toInt()}) are below the recommended "
                                    "threshold for ${r.finalRole}."
                              : "Your writing scores are solid. Keep building technical "
                                    "skills for ${r.finalRole}.",
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.text2,
                            height: 1.5,
                          ),
                        ),
                        const SizedBox(height: 10),
                        GestureDetector(
                          onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => SkillGapScreen(
                                report: r,
                                studentId: widget.studentId,
                              ),
                            ),
                          ),
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 12,
                              vertical: 8,
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.card,
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(color: AppColors.border),
                            ),
                            child: const Text(
                              "View full skill gap analysis →",
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                                color: AppColors.navy,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Quick actions
                  _sectionHeader("Quick Actions"),
                  Row(
                    children: [
                      Expanded(
                        child: _actionBtn(
                          "Job Roles",
                          Icons.work_outline,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => RolesScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _actionBtn(
                          "Education",
                          Icons.school_outlined,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => EducationScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: _actionBtn(
                          "Live Jobs",
                          Icons.business_center_outlined,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => JobsScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _actionBtn(
                          "Compare",
                          Icons.compare_arrows_rounded,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CompareScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: _actionBtn(
                          "Roadmap",
                          Icons.map_outlined,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => RoadmapScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _actionBtn(
                          "Writing Tips",
                          Icons.edit_note,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => WritingTipsScreen(report: r),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: _actionBtn(
                          "Share",
                          Icons.share_outlined,
                          () => _showShare(context, r),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _actionBtn(
                          "My Profile",
                          Icons.person_outline,
                          () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ProfileScreen(
                                studentId: widget.studentId,
                                report: r,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    child: _actionBtn(
                      "AI Explanation",
                      Icons.auto_awesome_outlined,
                      () => _showExplanation(context, r.finalExplanation),
                    ),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ── RIASEC Radar ──────────────────────────────────────────
  static const _riasecColors = {
    'R': AppColors.riasecR,
    'I': AppColors.riasecI,
    'A': AppColors.riasecA,
    'S': AppColors.riasecS,
    'E': AppColors.riasecE,
    'C': AppColors.riasecC,
  };

  Widget _buildRadarChart(Map<String, double> riasec) {
    final order = ['R', 'I', 'A', 'S', 'E', 'C'];
    final dataEntries = order
        .map((l) => RadarEntry(value: (riasec[l] ?? 50).clamp(0.0, 100.0)))
        .toList();

    return RadarChart(
      RadarChartData(
        radarShape: RadarShape.polygon,
        tickCount: 4,
        ticksTextStyle: const TextStyle(fontSize: 7, color: AppColors.text3),
        gridBorderData: const BorderSide(color: AppColors.border, width: 0.8),
        radarBorderData: const BorderSide(color: AppColors.border, width: 0.8),
        titlePositionPercentageOffset: 0.25,
        getTitle: (index, angle) {
          final letter = order[index];
          final val = (riasec[letter] ?? 50).toStringAsFixed(0);
          return RadarChartTitle(text: '$letter  $val', angle: 0);
        },
        dataSets: [
          RadarDataSet(
            dataEntries: dataEntries,
            fillColor: AppColors.riasecI.withOpacity(0.12),
            borderColor: AppColors.riasecI,
            borderWidth: 2.0,
            entryRadius: 5,
          ),
        ],
        radarBackgroundColor: Colors.transparent,
        borderData: FlBorderData(show: false),
        tickBorderData: const BorderSide(color: AppColors.border, width: 0.5),
      ),
      swapAnimationDuration: const Duration(milliseconds: 400),
    );
  }

  Widget _riasecLegend(String letter, String name, Color color, double score) =>
      Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          const SizedBox(width: 5),
          RichText(
            text: TextSpan(
              children: [
                TextSpan(
                  text: letter,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    color: color,
                  ),
                ),
                TextSpan(
                  text: ' — $name  ',
                  style: const TextStyle(fontSize: 10, color: AppColors.text2),
                ),
                TextSpan(
                  text: score.toStringAsFixed(0),
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w700,
                    color: color,
                  ),
                ),
              ],
            ),
          ),
        ],
      );

  Widget _radarInterpretationWidget(Map<String, double> riasec, String role) {
    final sorted = riasec.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    if (sorted.isEmpty) return const SizedBox();
    final top1 = sorted[0];
    final top2 = sorted[1];
    final bottom = sorted.last;
    const names = {
      'R': 'technical hands-on',
      'I': 'analytical data-driven',
      'A': 'creative innovative',
      'S': 'people-oriented',
      'E': 'leadership business',
      'C': 'structured organised',
    };
    final c1 = _riasecColors[top1.key] ?? AppColors.navy;
    final c2 = _riasecColors[top2.key] ?? AppColors.navy;
    final cb = _riasecColors[bottom.key] ?? AppColors.riasecS;

    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(10),
      ),
      child: RichText(
        text: TextSpan(
          style: const TextStyle(
            fontSize: 11,
            color: AppColors.text2,
            height: 1.5,
          ),
          children: [
            const TextSpan(text: 'Your radar extends strongly toward '),
            TextSpan(
              text: top1.key,
              style: TextStyle(fontWeight: FontWeight.w700, color: c1),
            ),
            TextSpan(text: ' (${top1.value.toStringAsFixed(0)}) and '),
            TextSpan(
              text: top2.key,
              style: TextStyle(fontWeight: FontWeight.w700, color: c2),
            ),
            TextSpan(text: ' (${top2.value.toStringAsFixed(0)}) '),
            TextSpan(text: '— ${names[top1.key]} and ${names[top2.key]}, '),
            TextSpan(text: 'confirming strong match for $role. Lower '),
            TextSpan(
              text: bottom.key,
              style: TextStyle(fontWeight: FontWeight.w700, color: cb),
            ),
            TextSpan(text: ' (${bottom.value.toStringAsFixed(0)}) '),
            TextSpan(text: 'reflects ${names[bottom.key]} is less dominant.'),
          ],
        ),
      ),
    );
  }

  String _interestCodeLabel(String code) {
    const labels = {
      'R': 'Realistic',
      'I': 'Investigative',
      'A': 'Artistic',
      'S': 'Social',
      'E': 'Enterprising',
      'C': 'Conventional',
    };
    return code.split('').map((l) => labels[l] ?? l).join(' · ');
  }

  // ── Composite tabs ────────────────────────────────────────
  static const _technicalKeys = [
    'Technical_ProblemSolving',
    'Tech_Adaptability',
    'Data_Literacy',
    'Process_Optimization',
  ];
  static const _analyticalKeys = [
    'Analytical_Thinking',
    'Career_Growth_Mindset',
    'Future_Orientation',
    'Strategic_Vision',
  ];
  static const _socialKeys = [
    'Social_Intelligence',
    'Communication_Skill',
    'Leadership_Capability',
    'Entrepreneurship_Orientation',
  ];
  static const _tabColors = [
    AppColors.compTechnical,
    AppColors.compAnalytical,
    AppColors.compSocial,
  ];

  Widget _compositeTabBtn(String label, int index) => GestureDetector(
    onTap: () => setState(() => _compositeTab = index),
    child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
      decoration: BoxDecoration(
        color: _compositeTab == index ? AppColors.navy : AppColors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: _compositeTab == index ? AppColors.navy : AppColors.border,
        ),
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: _compositeTab == index ? Colors.white : AppColors.text2,
        ),
      ),
    ),
  );

  List<Widget> _compositeRows(Map<String, double> composites) {
    final keys = _compositeTab == 0
        ? _technicalKeys
        : _compositeTab == 1
        ? _analyticalKeys
        : _socialKeys;
    final color = _tabColors[_compositeTab];
    return keys.where((k) => composites.containsKey(k)).map((k) {
      final val = composites[k]!;
      return Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Row(
          children: [
            SizedBox(
              width: 110,
              child: Text(
                k.replaceAll('_', ' '),
                style: const TextStyle(fontSize: 10, color: AppColors.text2),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: val / 100,
                  minHeight: 7,
                  backgroundColor: AppColors.surface,
                  valueColor: AlwaysStoppedAnimation(color),
                ),
              ),
            ),
            const SizedBox(width: 8),
            Text(
              '${val.toInt()}',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ],
        ),
      );
    }).toList();
  }

  // ── Helper widgets ────────────────────────────────────────
  Widget _sectionHeader(
    String title, {
    String? action,
    VoidCallback? onAction,
  }) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          title.toUpperCase(),
          style: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            color: AppColors.text3,
            letterSpacing: 0.5,
          ),
        ),
        if (action != null)
          GestureDetector(
            onTap: onAction,
            child: Text(
              action,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: AppColors.blue,
              ),
            ),
          ),
      ],
    ),
  );

  Widget _clusterChip(String label, Color bg, Color fg) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
    decoration: BoxDecoration(
      color: bg,
      borderRadius: BorderRadius.circular(20),
    ),
    child: Text(
      label.replaceAll('_', ' '),
      style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: fg),
    ),
  );

  Widget _scoreBar(
    String label,
    double value,
    Color color, {
    bool last = false,
  }) => Padding(
    padding: EdgeInsets.only(bottom: last ? 0 : 10),
    child: Row(
      children: [
        SizedBox(
          width: 74,
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w500,
              color: AppColors.text2,
            ),
          ),
        ),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: value / 100,
              minHeight: 7,
              backgroundColor: AppColors.surface,
              valueColor: AlwaysStoppedAnimation(color),
            ),
          ),
        ),
        const SizedBox(width: 8),
        Text(
          '${value.toInt()}',
          style: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            color: AppColors.navy,
          ),
        ),
      ],
    ),
  );

  Widget _statCard(String label, String value, String sub) => Container(
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(12),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label.toUpperCase(),
          style: const TextStyle(
            fontSize: 9,
            color: AppColors.text3,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.4,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: GoogleFonts.playfairDisplay(
            fontSize: 15,
            color: AppColors.navy,
            fontWeight: FontWeight.w700,
          ),
        ),
        Text(sub, style: const TextStyle(fontSize: 10, color: AppColors.text3)),
      ],
    ),
  );

  Widget _actionBtn(String label, IconData icon, VoidCallback onTap) =>
      GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(
            color: AppColors.card,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppColors.border),
          ),
          child: Column(
            children: [
              Icon(icon, color: AppColors.navy, size: 22),
              const SizedBox(height: 5),
              Text(
                label,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                  color: AppColors.text1,
                ),
              ),
            ],
          ),
        ),
      );

  String _fmt(int n) => n >= 1000 ? '${(n / 1000).toStringAsFixed(0)}K' : '$n';

  // ── Share bottom sheet ────────────────────────────────────
  void _showShare(BuildContext context, CareerReport r) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (_) => Padding(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Handle
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.border,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 20),

            // Title
            Text(
              "Share your report",
              style: GoogleFonts.playfairDisplay(
                fontSize: 22,
                fontWeight: FontWeight.w700,
                color: AppColors.navy,
              ),
            ),
            const SizedBox(height: 4),
            const Text(
              "Share your career guidance report",
              style: TextStyle(fontSize: 12, color: AppColors.text3),
            ),
            const SizedBox(height: 24),

            // Share buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                // Copy link
                _shareBtn(
                  bg: const Color(0xFF1877F2),
                  icon: Icons.copy_rounded,
                  label: "Copy link",
                  onTap: () {
                    Clipboard.setData(ClipboardData(text: _shareText));
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text("Report text copied to clipboard"),
                      ),
                    );
                  },
                ),
                // WhatsApp — opens real WhatsApp app
                _shareBtn(
                  bg: const Color(0xFF25D366),
                  icon: Icons.chat_rounded,
                  label: "WhatsApp",
                  onTap: () {
                    Navigator.pop(context);
                    _launchWhatsApp();
                  },
                ),
                // Email — opens real email app
                _shareBtn(
                  bg: const Color(0xFFEA4335),
                  icon: Icons.email_rounded,
                  label: "Email",
                  onTap: () {
                    Navigator.pop(context);
                    _launchEmail();
                  },
                ),
                // Save PDF
                _shareBtn(
                  bg: AppColors.navy,
                  icon: Icons.picture_as_pdf_rounded,
                  label: "Save PDF",
                  onTap: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Preview of what will be shared
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "WHAT WILL BE SHARED",
                    style: TextStyle(
                      fontSize: 9,
                      color: AppColors.text3,
                      fontWeight: FontWeight.w600,
                      letterSpacing: 0.5,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _shareText,
                    style: const TextStyle(
                      fontSize: 11,
                      color: AppColors.text2,
                      height: 1.5,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Close
            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: () => Navigator.pop(context),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  side: const BorderSide(color: AppColors.border),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  "Close",
                  style: TextStyle(color: AppColors.text2, fontSize: 14),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _shareBtn({
    required Color bg,
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) => GestureDetector(
    onTap: onTap,
    child: Column(
      children: [
        Container(
          width: 56,
          height: 56,
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Icon(icon, color: Colors.white, size: 26),
        ),
        const SizedBox(height: 6),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w500,
            color: AppColors.text2,
          ),
        ),
      ],
    ),
  );

  // ── AI Explanation ────────────────────────────────────────
  void _showExplanation(BuildContext context, String explanation) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 36,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.border,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 16),
            Text(
              "AI Explanation",
              style: GoogleFonts.playfairDisplay(
                fontSize: 20,
                fontWeight: FontWeight.w700,
                color: AppColors.navy,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              explanation,
              style: const TextStyle(
                fontSize: 13,
                color: AppColors.text2,
                height: 1.6,
              ),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}
