import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../config/app_constants.dart';
import '../services/api_service.dart';
import 'writing_screen.dart';

class MCQScreen extends StatefulWidget {
  final String studentId;
  final String assessmentId;
  const MCQScreen({
    super.key,
    this.studentId = "STU001",
    required this.assessmentId,
  });
  @override
  State<MCQScreen> createState() => _MCQScreenState();
}

class _MCQScreenState extends State<MCQScreen> {
  int _current = 0;
  final List<int> _answers = List.filled(40, 0);
  bool _loading = false;

  void _pick(int val) => setState(() => _answers[_current] = val);

  Future<void> _next() async {
    if (_answers[_current] == 0) _pick(3);
    if (_current < 39) {
      setState(() => _current++);
    } else {
      await _submit();
    }
  }

  void _back() {
    if (_current > 0) setState(() => _current--);
  }

  Future<void> _submit() async {
    setState(() => _loading = true);
    try {
      // Build answers map
      final Map<String, dynamic> answers = {};
      for (int i = 0; i < 40; i++) {
        answers['Q${i + 1}'] = _answers[i] == 0 ? 3 : _answers[i];
      }

      // Use v2 endpoint — saves under assessmentId
      final result =
          await ApiService.submitMCQv2(widget.assessmentId, answers);

      if (result['status'] == 'error') {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${result['message']}'),
              backgroundColor: AppColors.rose,
              duration: const Duration(seconds: 3),
            ),
          );
        }
        return;
      }

      if (mounted)
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => WritingScreen(
              studentId:    widget.studentId,
              assessmentId: widget.assessmentId,
            ),
          ),
        );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text('Error: $e'),
              backgroundColor: AppColors.rose),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final pct      = (_current / 40 * 100).round();
    final section  = AppConstants.getSectionForQuestion(_current);
    final question = AppConstants.questions[_current];

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Column(
        children: [
          // ── Header ──────────────────────────────────────
          Container(
            color: AppColors.navy,
            padding: const EdgeInsets.fromLTRB(22, 54, 22, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      "Career Assessment",
                      style: GoogleFonts.playfairDisplay(
                        fontSize: 20,
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    Text(
                      "${_current + 1}/40",
                      style: TextStyle(
                        color: Colors.white.withOpacity(0.7),
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: pct / 100,
                    minHeight: 5,
                    backgroundColor: Colors.white.withOpacity(0.15),
                    valueColor: const AlwaysStoppedAnimation<Color>(
                        Color(0xFF60A5FA)),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  section,
                  style: TextStyle(
                    fontSize: 11,
                    color: Colors.white.withOpacity(0.55),
                    letterSpacing: 0.3,
                  ),
                ),
              ],
            ),
          ),

          // ── Question ─────────────────────────────────────
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 8),
                  Text(
                    question,
                    style: GoogleFonts.plusJakartaSans(
                      fontSize: 17,
                      color: AppColors.text1,
                      fontWeight: FontWeight.w500,
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 28),
                  ...List.generate(5, (i) {
                    final val = i + 1;
                    final labels = [
                      "Strongly Disagree",
                      "Disagree",
                      "Neutral",
                      "Agree",
                      "Strongly Agree",
                    ];
                    final selected = _answers[_current] == val;
                    return GestureDetector(
                      onTap: () => _pick(val),
                      child: Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 14),
                        decoration: BoxDecoration(
                          color: selected
                              ? AppColors.navy
                              : AppColors.card,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: selected
                                ? AppColors.navy
                                : AppColors.border,
                            width: selected ? 1.5 : 1,
                          ),
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 28,
                              height: 28,
                              decoration: BoxDecoration(
                                color: selected
                                    ? Colors.white.withOpacity(0.2)
                                    : AppColors.surface,
                                shape: BoxShape.circle,
                              ),
                              child: Center(
                                child: Text(
                                  "$val",
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w700,
                                    color: selected
                                        ? Colors.white
                                        : AppColors.text2,
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Text(
                              labels[i],
                              style: TextStyle(
                                fontSize: 14,
                                color: selected
                                    ? Colors.white
                                    : AppColors.text1,
                                fontWeight: selected
                                    ? FontWeight.w600
                                    : FontWeight.w400,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                ],
              ),
            ),
          ),

          // ── Navigation buttons ────────────────────────────
          Container(
            padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
            decoration: BoxDecoration(
              color: AppColors.card,
              border: const Border(
                  top: BorderSide(color: AppColors.border)),
            ),
            child: Row(
              children: [
                if (_current > 0)
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _back,
                      style: OutlinedButton.styleFrom(
                        padding:
                            const EdgeInsets.symmetric(vertical: 14),
                        side:
                            const BorderSide(color: AppColors.border),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text("Back",
                          style: TextStyle(color: AppColors.text2)),
                    ),
                  ),
                if (_current > 0) const SizedBox(width: 12),
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _loading ? null : _next,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.navy,
                      padding:
                          const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _loading
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                                color: Colors.white, strokeWidth: 2),
                          )
                        : Text(
                            _current < 39 ? "Next" : "Submit",
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
        ],
      ),
    );
  }
}
