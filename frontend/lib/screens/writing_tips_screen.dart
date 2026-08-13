import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';

// =============================================================
// Writing Analysis Results Screen
// Replaced from: writing analysis Screen
//
// Shows what M2 Writing Analysis model found in the student's
// own writing sample. Based on actual cosine similarity scores
// from Sentence Transformer analysis against career-readiness
// anchor sentences.
//
// Does NOT give writing advice — that is outside the scope
// of a career guidance platform.
// =============================================================

class WritingTipsScreen extends StatelessWidget {
  final CareerReport report;
  const WritingTipsScreen({super.key, required this.report});

  @override
  Widget build(BuildContext context) {
    final overall = report.overallWritingScore;
    final role = report.finalRole;

    final traits = [
      {
        "name": "Analytical Thinking",
        "score": report.writingAnalytical,
        "icon": Icons.psychology_outlined,
        "desc":
            "How strongly your writing demonstrates logical reasoning and data-driven thinking.",
      },
      {
        "name": "Clarity",
        "score": report.writingClarity,
        "icon": Icons.lightbulb_outline,
        "desc":
            "How clearly and precisely your ideas are expressed in writing.",
      },
      {
        "name": "Structure",
        "score": report.writingStructure,
        "icon": Icons.format_list_bulleted,
        "desc": "How well-organised and coherent your writing is.",
      },
      {
        "name": "Confidence",
        "score": report.writingConfidence,
        "icon": Icons.trending_up,
        "desc":
            "How assertively and decisively your career intent is expressed.",
      },
      {
        "name": "Creativity",
        "score": report.writingCreativity,
        "icon": Icons.brush_outlined,
        "desc": "How original and inventive your thinking appears in writing.",
      },
    ];

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "Writing Analysis",
          style: GoogleFonts.playfairDisplay(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.navy,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Your Writing Profile",
                    style: GoogleFonts.playfairDisplay(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    "Based on AI analysis of your writing sample using career-readiness assessment.",
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.75),
                      fontSize: 13,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "${overall.toStringAsFixed(1)}/100",
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 36,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          Text(
                            "Overall Score",
                            style: TextStyle(
                              color: Colors.white.withOpacity(0.7),
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 14,
                          vertical: 8,
                        ),
                        decoration: BoxDecoration(
                          color: _overallColor(overall).withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: _overallColor(overall).withOpacity(0.5),
                          ),
                        ),
                        child: Text(
                          _overallLabel(overall),
                          style: TextStyle(
                            color: _overallColor(overall),
                            fontWeight: FontWeight.w600,
                            fontSize: 14,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Role context
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.card,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.border),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.work_outline,
                    color: AppColors.blue,
                    size: 20,
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      "Recommended role: $role",
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w500,
                        color: AppColors.text1,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            Text(
              "Trait Breakdown",
              style: GoogleFonts.playfairDisplay(
                fontSize: 17,
                fontWeight: FontWeight.w700,
                color: AppColors.text1,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              "Each trait was assessed by comparing your writing to career-readiness anchor sentences using Sentence Transformers.",
              style: TextStyle(fontSize: 12, color: AppColors.text3),
            ),
            const SizedBox(height: 14),

            // Trait cards
            ...traits.map(
              (t) => _traitCard(
                t["name"] as String,
                (t["score"] as double),
                t["icon"] as IconData,
                t["desc"] as String,
              ),
            ),

            const SizedBox(height: 20),

            // Disclaimer
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.border),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(
                    Icons.info_outline,
                    color: AppColors.text3,
                    size: 16,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      "These scores reflect how your writing sample expressed career-readiness traits relevant to IT roles. They are one component of your overall career guidance report and should be read alongside your psychological profile and market demand data.",
                      style: TextStyle(
                        fontSize: 11,
                        color: AppColors.text3,
                        height: 1.5,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _traitCard(String name, double score, IconData icon, String desc) {
    final color = _traitColor(score);
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  name,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.text1,
                  ),
                ),
              ),
              Text(
                "${score.toStringAsFixed(1)}/100",
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                  color: color,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: score / 100,
              minHeight: 6,
              backgroundColor: AppColors.border,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
          const SizedBox(height: 10),
          Text(
            desc,
            style: TextStyle(fontSize: 12, color: AppColors.text3, height: 1.4),
          ),
        ],
      ),
    );
  }

  Color _traitColor(double score) {
    if (score >= 70) return const Color(0xFF4CAF50);
    if (score >= 50) return AppColors.blue;
    return const Color(0xFFFF9800);
  }

  Color _overallColor(double score) {
    if (score >= 70) return const Color(0xFF4CAF50);
    if (score >= 50) return AppColors.blue;
    return const Color(0xFFFF9800);
  }

  String _overallLabel(double score) {
    if (score >= 70) return "Strong Profile";
    if (score >= 50) return "Developing Profile";
    return "Early Stage";
  }
}
