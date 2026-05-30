import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../services/api_service.dart';
import 'processing_screen.dart';

class WritingScreen extends StatefulWidget {
  final String studentId;
  const WritingScreen({super.key, required this.studentId});
  @override
  State<WritingScreen> createState() => _WritingScreenState();
}

class _WritingScreenState extends State<WritingScreen> {
  final _ctrl = TextEditingController();
  bool _loading = false;
  int _wordCount = 0;

  @override
  void initState() {
    super.initState();
    _ctrl.addListener(
      () => setState(
        () => _wordCount = _ctrl.text.trim().isEmpty
            ? 0
            : _ctrl.text.trim().split(RegExp(r'\s+')).length,
      ),
    );
  }

  Color get _wcColor {
    if (_wordCount >= 100 && _wordCount <= 150) return AppColors.mint;
    if (_wordCount > 150) return AppColors.rose;
    return AppColors.gold;
  }

  Future<void> _submit() async {
    if (_wordCount < 10) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please write at least 10 words'),
          backgroundColor: AppColors.rose,
        ),
      );
      return;
    }
    setState(() => _loading = true);
    try {
      await ApiService.submitWriting(widget.studentId, _ctrl.text.trim());
      await ApiService.generateReport(widget.studentId);
      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => ProcessingScreen(studentId: widget.studentId),
          ),
        );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.rose),
      );
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(24, 60, 24, 24),
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Writing sample",
                  style: GoogleFonts.playfairDisplay(
                    fontSize: 28,
                    color: Colors.white,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                Text(
                  "Final step before your career report",
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.white.withOpacity(0.5),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Prompt box
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.bluePale,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.blueMid),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Answer this Question:",
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: AppColors.blue,
                            letterSpacing: 0.5,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          '"Describe a challenge you faced recently. What did you do and what did you learn from it?"',
                          style: TextStyle(
                            fontSize: 13,
                            color: AppColors.navy,
                            height: 1.55,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Text area
                  TextField(
                    controller: _ctrl,
                    maxLines: 10,
                    decoration: InputDecoration(
                      hintText: "Start writing here... (aim for 100–150 words)",
                      hintStyle: const TextStyle(
                        color: AppColors.text3,
                        fontSize: 13,
                      ),
                      filled: true,
                      fillColor: AppColors.card,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(14),
                        borderSide: const BorderSide(color: AppColors.border),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(14),
                        borderSide: const BorderSide(color: AppColors.border),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(14),
                        borderSide: const BorderSide(
                          color: AppColors.blue,
                          width: 1.5,
                        ),
                      ),
                      contentPadding: const EdgeInsets.all(16),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Word count",
                        style: TextStyle(fontSize: 11, color: AppColors.text3),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 10,
                          vertical: 3,
                        ),
                        decoration: BoxDecoration(
                          color: _wcColor.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          "$_wordCount words",
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: _wcColor,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const Divider(height: 24, color: AppColors.border),
                  // Tips
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "TIPS FOR A STRONG RESPONSE",
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w600,
                            color: AppColors.text3,
                            letterSpacing: 0.5,
                          ),
                        ),
                        const SizedBox(height: 8),
                        ...[
                          "Be specific about what you did",
                          "Mention what you learned from the experience",
                          "Write in clear, structured sentences",
                        ].map(
                          (t) => Padding(
                            padding: const EdgeInsets.only(bottom: 5),
                            child: Row(
                              children: [
                                const Icon(
                                  Icons.check_circle,
                                  color: AppColors.mint,
                                  size: 14,
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  t,
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.text2,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _loading ? null : _submit,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.navy,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      child: _loading
                          ? const CircularProgressIndicator(
                              color: Colors.white,
                              strokeWidth: 2,
                            )
                          : Text(
                              "Submit & generate report →",
                              style: GoogleFonts.plusJakartaSans(
                                fontSize: 15,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
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
}
