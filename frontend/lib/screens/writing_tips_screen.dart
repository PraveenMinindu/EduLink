import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_colors.dart';
import '../../models/career_report_model.dart';

class WritingTipsScreen extends StatelessWidget {
  final CareerReport report;
  const WritingTipsScreen({super.key, required this.report});

  @override
  Widget build(BuildContext context) {
    final traits = [
      {
        "name": "Clarity",
        "score": report.writingClarity,
        "color": AppColors.blue,
        "tip":
            "Use shorter sentences (max 20 words). Start each paragraph with a clear topic sentence. Avoid vague words like 'things' or 'stuff' — be specific.",
        "example":
            "Weak: \"I did some data work and found things.\"\nStrong: \"I used Python's pandas library to clean a 1,000-row dataset and identify three key trends.\"",
      },
      {
        "name": "Analytical",
        "score": report.writingAnalytical,
        "color": AppColors.blue,
        "tip":
            "Show analytical reasoning by using evidence, comparisons, and cause-effect relationships. Your writing naturally supports data-focused roles.",
        "example":
            "Add phrases like: \"After comparing X and Y, I found that...\"\nor \"This resulted in... because...\"",
      },
      {
        "name": "Structure",
        "score": report.writingStructure,
        "color": AppColors.violet,
        "tip":
            "Use a clear beginning, middle, and end. Link paragraphs with transition words like 'however', 'therefore', 'as a result'.",
        "example":
            "Template: Situation → Challenge → Action I took → What I learned → Outcome",
      },
      {
        "name": "Confidence",
        "score": report.writingConfidence,
        "color": AppColors.violet,
        "tip":
            "Replace uncertain language with assertive statements. Avoid 'I think maybe' or 'I hope to'. Use active voice and definite statements.",
        "example":
            "Weak: \"I tried to learn Python and maybe got better at it.\"\nStrong: \"I learned Python fundamentals in 3 weeks and built a working data analysis script.\"",
      },
      {
        "name": "Creativity",
        "score": report.writingCreativity,
        "color": AppColors.mint,
        "tip":
            "Show creative thinking by describing unusual approaches or original ideas. Explain what made your solution unique rather than following a standard path.",
        "example":
            "Describe how you combined two unrelated ideas, tried an unconventional approach, or invented your own solution rather than copying an existing one.",
      },
    ];

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
                    Text("Report",
                        style:
                            TextStyle(color: Colors.white54, fontSize: 13)),
                  ]),
                ),
                const SizedBox(height: 12),
                Text("Writing improvement",
                    style: GoogleFonts.playfairDisplay(
                        fontSize: 26,
                        color: Colors.white,
                        fontWeight: FontWeight.w700)),
                Text("Personalised tips for each writing trait",
                    style: TextStyle(
                        fontSize: 12,
                        color: Colors.white.withOpacity(0.5))),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: traits.length,
              itemBuilder: (_, i) {
                final t = traits[i];
                final score = t["score"] as double;
                final color = t["color"] as Color;
                String level;
                Color levelBg, levelFg;
                if (score >= 70) {
                  level = "Strong";
                  levelBg = AppColors.mintPale;
                  levelFg = AppColors.mint;
                } else if (score >= 55) {
                  level = "Developing";
                  levelBg = AppColors.goldPale;
                  levelFg = AppColors.gold;
                } else {
                  level = "Needs work";
                  levelBg = AppColors.rosePale;
                  levelFg = AppColors.rose;
                }

                return Container(
                  margin: const EdgeInsets.only(bottom: 12),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.card,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppColors.border),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Trait header
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(t["name"] as String,
                              style: const TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.text1)),
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                                color: levelBg,
                                borderRadius: BorderRadius.circular(20)),
                            child: Text("$level · ${score.toInt()}",
                                style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w700,
                                    color: levelFg)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      // Progress bar
                      ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: score / 100,
                          minHeight: 7,
                          backgroundColor: AppColors.surface,
                          valueColor: AlwaysStoppedAnimation(color),
                        ),
                      ),
                      const SizedBox(height: 12),
                      // Tip box
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                            color: AppColors.surface,
                            borderRadius: BorderRadius.circular(10)),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              score >= 70
                                  ? "YOUR STRENGTH"
                                  : "HOW TO IMPROVE",
                              style: TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w700,
                                  color: color,
                                  letterSpacing: 0.4),
                            ),
                            const SizedBox(height: 6),
                            Text(t["tip"] as String,
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.text2,
                                    height: 1.6)),
                          ],
                        ),
                      ),
                      const SizedBox(height: 8),
                      // Example box
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          border: Border(
                              left: BorderSide(color: color, width: 3)),
                          color: color.withOpacity(0.04),
                          borderRadius: const BorderRadius.only(
                            topRight: Radius.circular(8),
                            bottomRight: Radius.circular(8),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text("EXAMPLE",
                                style: TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.w700,
                                    color: color,
                                    letterSpacing: 0.4)),
                            const SizedBox(height: 5),
                            Text(t["example"] as String,
                                style: const TextStyle(
                                    fontSize: 11,
                                    color: AppColors.text2,
                                    height: 1.55)),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
