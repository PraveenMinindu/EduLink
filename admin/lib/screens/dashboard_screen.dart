// =============================================================
// EduLink Admin — Dashboard Screen
// Fix 7:  Recent activity hidden for MVP
// Fix 11: ErrorView widget used instead of inline error card
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../services/api_service.dart';
import '../widgets/error_view.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? _stats;
  bool    _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; });
    try {
      final stats = await ApiService.getStats();
      setState(() { _stats = stats; _loading = false; });
    } catch (e) {
      setState(() {
        _error   = e.toString().replaceFirst('Exception: ', '');
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Page header
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Dashboard',
                      style: GoogleFonts.plusJakartaSans(
                        fontSize:   22,
                        fontWeight: FontWeight.w700,
                        color:      AppColors.text1,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      'Education knowledge base overview',
                      style: GoogleFonts.plusJakartaSans(
                        fontSize: 13,
                        color:    AppColors.text3,
                      ),
                    ),
                  ],
                ),
              ),
              IconButton(
                onPressed: _load,
                icon:    const Icon(Icons.refresh, color: AppColors.text3),
                tooltip: 'Refresh',
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Fix 10: Loading indicator
          if (_loading)
            const Center(
              child: Padding(
                padding: EdgeInsets.all(48),
                child: CircularProgressIndicator(color: AppColors.sky),
              ),
            )
          // Fix 11: Reusable ErrorView with Retry
          else if (_error != null)
            ErrorView(message: _error!, onRetry: _load)
          else
            _content(),
        ],
      ),
    );
  }

  Widget _content() {
    final unis  = _stats!['universities'] as Map<String, dynamic>;
    final progs = _stats!['programs']     as Map<String, dynamic>;
    final reps  = _stats!['reports']      as Map<String, dynamic>;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Stat cards row
        LayoutBuilder(builder: (ctx, c) {
          // Fix: cards were forced into a fixed aspect ratio, so on
          // narrower widths (tablets, small windows) the fixed height
          // was shorter than the content needed, causing bottom
          // overflow. Sizing height to content (no aspect ratio) and
          // adding a tablet breakpoint fixes both the overflow and
          // the abrupt 1-col -> 3-col jump at 600px.
          int cols = 1;
          if (c.maxWidth > 900) {
            cols = 3;
          } else if (c.maxWidth > 600) {
            cols = 2;
          }
          const spacing = 12.0;
          final cardWidth =
              (c.maxWidth - spacing * (cols - 1)) / cols;
          final cards = [
            _statCard(
              icon:  Icons.account_balance_outlined,
              color: AppColors.sky,
              value: '${unis['total']  ?? 0}',
              label: 'Universities',
              sub:   '${unis['active'] ?? 0} active',
            ),
            _statCard(
              icon:  Icons.school_outlined,
              color: AppColors.mint,
              value: '${progs['total']         ?? 0}',
              label: 'Degree programs',
              sub:   '${progs['activePercent'] ?? 0}% active',
            ),
            _statCard(
              icon:  Icons.analytics_outlined,
              color: AppColors.violet,
              value: '${reps['total'] ?? 0}',
              label: 'Student reports',
              sub:   'generated to date',
            ),
          ];
          return Wrap(
            spacing:    spacing,
            runSpacing: spacing,
            children: [
              for (final card in cards)
                SizedBox(width: cardWidth, child: card),
            ],
          );
        }),

        // Fix 7: Recent activity hidden for MVP
        // Uncomment the block below in a future version
        //
        // const SizedBox(height: 24),
        // Text('Recent activity', ...),
        // ...activityList,
      ],
    );
  }

  Widget _statCard({
    required IconData icon,
    required Color    color,
    required String   value,
    required String   label,
    required String   sub,
  }) =>
      Container(
        decoration: BoxDecoration(
          color:        AppColors.card,
          borderRadius: BorderRadius.circular(14),
          border:       Border.all(color: AppColors.border),
        ),
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment:  MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: 10),
            Text(
              value,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   30,
                fontWeight: FontWeight.w700,
                color:      AppColors.text1,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              label,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   12,
                fontWeight: FontWeight.w500,
                color:      AppColors.text3,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              sub,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 11, color: color),
            ),
          ],
        ),
      );
}
