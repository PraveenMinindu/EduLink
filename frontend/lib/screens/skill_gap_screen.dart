import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;
import '../../config/app_colors.dart';
import '../../config/app_constants.dart';
import '../../models/career_report_model.dart';

class SkillGapScreen extends StatefulWidget {
  final CareerReport report;
  final String studentId;

  const SkillGapScreen({
    super.key,
    required this.report,
    required this.studentId,
  });

  @override
  State<SkillGapScreen> createState() => _SkillGapScreenState();
}

class _SkillGapScreenState extends State<SkillGapScreen> {
  List<dynamic> _skills    = [];
  bool          _loading   = true;
  bool          _hasError  = false;
  String        _source    = '';
  int           _totalJobs = 0;

  @override
  void initState() {
    super.initState();
    _loadSkills();
  }

  Future<void> _loadSkills() async {
    try {
      final response = await http.get(
        Uri.parse(
          "${AppConstants.baseUrl}/student/skills/${widget.studentId}",
        ),
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body)['data'];
        setState(() {
          _skills    = List<dynamic>.from(data['skills'] ?? []);
          _source    = data['source'] ?? '';
          _totalJobs = data['total_jobs'] ?? 0;
          _loading   = false;
        });
      } else {
        setState(() {
          _loading  = false;
          _hasError = true;
        });
      }
    } catch (e) {
      setState(() {
        _loading  = false;
        _hasError = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final role = widget.report.finalRole;

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
                Text("Skill gap analysis",
                    style: GoogleFonts.playfairDisplay(
                        fontSize: 26,
                        color: Colors.white,
                        fontWeight: FontWeight.w700)),
                Text("What to develop for $role",
                    style: TextStyle(
                        fontSize: 12,
                        color: Colors.white.withOpacity(0.5))),
              ],
            ),
          ),

          // Body
          Expanded(
            child: _loading
                ? const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(
                            color: AppColors.blue),
                        SizedBox(height: 16),
                        Text("Fetching real job market data...",
                            style: TextStyle(
                                color: AppColors.text3,
                                fontSize: 13)),
                      ],
                    ),
                  )
                : _hasError
                    ? _buildError()
                    : _buildContent(role),
          ),
        ],
      ),
    );
  }

  Widget _buildError() => Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.wifi_off,
                  color: AppColors.text3, size: 48),
              const SizedBox(height: 16),
              const Text("Could not load skill data",
                  style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: AppColors.text1)),
              const SizedBox(height: 8),
              const Text(
                "Check your connection and try again",
                style:
                    TextStyle(fontSize: 13, color: AppColors.text3),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    _loading  = true;
                    _hasError = false;
                  });
                  _loadSkills();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.blue,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text("Try again",
                    style: TextStyle(color: Colors.white)),
              ),
            ],
          ),
        ),
      );

  Widget _buildContent(String role) {
    final technical =
        _skills.where((s) => s['type'] == 'technical').toList();
    final soft =
        _skills.where((s) => s['type'] == 'soft').toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Summary card
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.navyLight,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("Role target: $role",
                    style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: Colors.white)),
                const SizedBox(height: 6),
                Text(
                  "${_skills.length} skills identified from $_totalJobs real job postings",
                  style: TextStyle(
                      fontSize: 12,
                      color: Colors.white.withOpacity(0.6),
                      height: 1.5),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),

          // Data source badge
          Container(
            padding: const EdgeInsets.symmetric(
                horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: _source == 'adzuna_live'
                  ? AppColors.mintPale
                  : AppColors.goldPale,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: _source == 'adzuna_live'
                    ? AppColors.mint.withOpacity(0.3)
                    : AppColors.gold.withOpacity(0.3),
              ),
            ),
            child: Row(children: [
              Icon(
                _source == 'adzuna_live'
                    ? Icons.cloud_done_outlined
                    : Icons.storage_outlined,
                size: 14,
                color: _source == 'adzuna_live'
                    ? AppColors.mint
                    : AppColors.gold,
              ),
              const SizedBox(width: 6),
              Text(
                _source == 'adzuna_live'
                    ? "Live data from $_totalJobs real job postings (India / Sri Lanka)"
                    : "Based on industry knowledge for this career cluster",
                style: TextStyle(
                  fontSize: 11,
                  color: _source == 'adzuna_live'
                      ? AppColors.mint
                      : AppColors.gold,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ]),
          ),
          const SizedBox(height: 16),

          // Technical skills
          if (technical.isNotEmpty) ...[
            _sectionLabel("TECHNICAL SKILLS REQUIRED",
                AppColors.blue),
            const SizedBox(height: 8),
            ...technical.map((s) => _skillCard(s, AppColors.blue)),
            const SizedBox(height: 16),
          ],

          // Soft skills
          if (soft.isNotEmpty) ...[
            _sectionLabel("SOFT SKILLS REQUIRED", AppColors.violet),
            const SizedBox(height: 8),
            ...soft.map((s) => _skillCard(s, AppColors.violet)),
            const SizedBox(height: 16),
          ],

          // Writing strengths
          _buildStrengthsCard(),
        ],
      ),
    );
  }

  Widget _sectionLabel(String text, Color color) => Text(
        text,
        style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w700,
            color: color,
            letterSpacing: 0.5),
      );

  Widget _skillCard(dynamic skill, Color color) {
    final frequency = (skill['frequency'] ?? 0) as int;
    final name      = skill['name'] ?? '';

    String level;
    String advice;
    Color  levelColor;
    Color  levelBg;

    if (frequency >= 70) {
      level      = "High demand";
      advice     = "Learn this first — appears in most job postings";
      levelColor = AppColors.rose;
      levelBg    = AppColors.rosePale;
    } else if (frequency >= 40) {
      level      = "Moderate demand";
      advice     = "Commonly required — build this skill next";
      levelColor = AppColors.gold;
      levelBg    = AppColors.goldPale;
    } else {
      level      = "Good to know";
      advice     = "Useful for this role — learn when ready";
      levelColor = AppColors.mint;
      levelBg    = AppColors.mintPale;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(name,
                    style: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                        color: AppColors.text1)),
              ),
              Row(children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: levelBg,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(level,
                      style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w600,
                          color: levelColor)),
                ),
                const SizedBox(width: 6),
                Text("$frequency%",
                    style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                        color: AppColors.navy)),
              ]),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: frequency / 100,
              minHeight: 6,
              backgroundColor: AppColors.surface,
              valueColor: AlwaysStoppedAnimation(color),
            ),
          ),
          const SizedBox(height: 6),
          Text(advice,
              style: const TextStyle(
                  fontSize: 11, color: AppColors.text3)),
        ],
      ),
    );
  }

  Widget _buildStrengthsCard() {
    final strengths = <String>[];

    if (widget.report.writingAnalytical >= 65)
      strengths.add(
          "Analytical ${widget.report.writingAnalytical.toInt()}%");
    if (widget.report.writingClarity >= 65)
      strengths
          .add("Clarity ${widget.report.writingClarity.toInt()}%");
    if (widget.report.writingStructure >= 65)
      strengths.add(
          "Structure ${widget.report.writingStructure.toInt()}%");
    if (widget.report.writingConfidence >= 65)
      strengths.add(
          "Confidence ${widget.report.writingConfidence.toInt()}%");
    if (strengths.isEmpty) strengths.add("Assessment completed");

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.mintPale,
        borderRadius: BorderRadius.circular(16),
        border:
            Border.all(color: AppColors.mint.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("YOUR WRITING STRENGTHS ✓",
              style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: AppColors.mint,
                  letterSpacing: 0.5)),
          const SizedBox(height: 10),
          Wrap(
            spacing: 7,
            runSpacing: 7,
            children: strengths
                .map((s) => Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 5),
                      decoration: BoxDecoration(
                        color: AppColors.mint.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(s,
                          style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: AppColors.mint)),
                    ))
                .toList(),
          ),
        ],
      ),
    );
  }
}
