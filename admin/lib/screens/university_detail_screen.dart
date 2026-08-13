// =============================================================
// EduLink Admin — University Detail Screen (Central Workspace)
// Fix 1:  Removed redundant skyMid getter
// Fix 11: ErrorView used instead of inline error text
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/university.dart';
import '../models/degree_program.dart';
import '../services/api_service.dart';
import '../widgets/error_view.dart';
import 'university_form_screen.dart';
import 'program_form_screen.dart';

class UniversityDetailScreen extends StatefulWidget {
  final University university;
  const UniversityDetailScreen({super.key, required this.university});

  @override
  State<UniversityDetailScreen> createState() =>
      _UniversityDetailScreenState();
}

class _UniversityDetailScreenState
    extends State<UniversityDetailScreen> {
  late University     _university;
  List<DegreeProgram> _programs     = [];
  bool                _loadingProgs = true;
  String?             _error;

  @override
  void initState() {
    super.initState();
    _university = widget.university;
    _loadPrograms();
  }

  Future<void> _loadPrograms() async {
    setState(() { _loadingProgs = true; _error = null; });
    try {
      final list =
          await ApiService.getPrograms(universityId: _university.id);
      setState(() { _programs = list; _loadingProgs = false; });
    } catch (e) {
      setState(() {
        _error        = e.toString().replaceFirst('Exception: ', '');
        _loadingProgs = false;
      });
    }
  }

  Future<void> _deactivateProgram(DegreeProgram p) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: Text(
          'Deactivate program',
          style: GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w700),
        ),
        content: Text(
          'Deactivate "${p.degreeName}"?\n\n'
          'The program will be set to Inactive and can be reactivated later.',
          style: GoogleFonts.plusJakartaSans(fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.rose,
                foregroundColor: Colors.white),
            child: const Text('Deactivate'),
          ),
        ],
      ),
    );

    if (ok != true) return;
    try {
      await ApiService.deactivateProgram(p.id);
      _loadPrograms();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(
            e.toString().replaceFirst('Exception: ', ''),
            style: GoogleFonts.plusJakartaSans(),
          ),
          backgroundColor: AppColors.rose,
        ));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        foregroundColor: Colors.white,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              _university.name,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   15,
                fontWeight: FontWeight.w700,
                color:      Colors.white,
              ),
            ),
            Text(
              '${_university.type} · ${_university.location}',
              style: GoogleFonts.plusJakartaSans(
                fontSize: 11,
                color:    const Color(0xFF6B87C4),
              ),
            ),
          ],
        ),
        actions: [
          Container(
            margin:  const EdgeInsets.symmetric(vertical: 12),
            padding: const EdgeInsets.symmetric(
                horizontal: 10, vertical: 2),
            decoration: BoxDecoration(
              color:        _university.isActive
                  ? AppColors.mintPale
                  : AppColors.surface,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              _university.status,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   11,
                fontWeight: FontWeight.w600,
                color:      _university.isActive
                    ? const Color(0xFF065F46)
                    : AppColors.text3,
              ),
            ),
          ),
          const SizedBox(width: 8),
          TextButton.icon(
            onPressed: () async {
              final updated = await Navigator.push<bool>(
                context,
                MaterialPageRoute(
                  builder: (_) =>
                      UniversityFormScreen(university: _university),
                ),
              );
              if (updated == true) {
                final u =
                    await ApiService.getUniversity(_university.id);
                setState(() => _university = u);
                _loadPrograms();
              }
            },
            icon:  const Icon(Icons.edit_outlined,
                size: 16, color: Colors.white),
            label: Text(
              'Edit',
              style: GoogleFonts.plusJakartaSans(
                  color: Colors.white, fontWeight: FontWeight.w500),
            ),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Info + map row
            LayoutBuilder(builder: (ctx, c) {
              final wide = c.maxWidth > 700;
              return wide
                  ? Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(child: _infoCard()),
                        const SizedBox(width: 14),
                        Expanded(child: _mapCard()),
                      ],
                    )
                  : Column(children: [
                      _infoCard(),
                      const SizedBox(height: 14),
                      _mapCard(),
                    ]);
            }),
            const SizedBox(height: 20),

            // Programs section
            _programsSection(),
          ],
        ),
      ),
    );
  }

  Widget _infoCard() => _card(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _cardHeader('University info'),
            _infoRow('Type',     _university.type),
            _infoRow('Location', _university.location),
            if (_university.website.isNotEmpty)
              _infoRow('Website', _university.website, highlight: true),
            _infoRow('Status', _university.status),
            if (_university.shortDescription.isNotEmpty) ...[
              const SizedBox(height: 10),
              Text(
                _university.shortDescription,
                style: GoogleFonts.plusJakartaSans(
                    fontSize: 12, color: AppColors.text2, height: 1.5),
              ),
            ],
          ],
        ),
      );

  Widget _mapCard() => _card(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _cardHeader('Campus location'),
            Container(
              height: 120,
              decoration: BoxDecoration(
                color:        AppColors.skyPale,
                borderRadius: BorderRadius.circular(10),
                // Fix 1: use AppColors.skyMid directly — no redundant getter
                border: Border.all(color: AppColors.skyMid),
              ),
              child: const Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.location_on_outlined,
                        color: AppColors.sky, size: 32),
                    SizedBox(height: 6),
                    Text(
                      'OpenStreetMap — Phase 4',
                      style: TextStyle(
                          fontSize: 12, color: AppColors.sky),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      );

  Widget _programsSection() => _card(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _cardHeader(
              'Degree programs (${_programs.length})',
              action: ElevatedButton.icon(
                onPressed: () async {
                  final created = await Navigator.push<bool>(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          ProgramFormScreen(university: _university),
                    ),
                  );
                  if (created == true) {
                    _loadPrograms();
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Program added successfully.',
                              style: GoogleFonts.plusJakartaSans()),
                          backgroundColor: AppColors.mint,
                        ),
                      );
                    }
                  }
                },
                icon:  const Icon(Icons.add, size: 14),
                label: const Text('Add program'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.sky,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                      horizontal: 14, vertical: 8),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8)),
                  textStyle: GoogleFonts.plusJakartaSans(
                      fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ),
            ),
            const SizedBox(height: 10),

            // Fix 10: Loading indicator
            if (_loadingProgs)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(24),
                  child:
                      CircularProgressIndicator(color: AppColors.sky),
                ),
              )
            // Fix 11: ErrorView with Retry
            else if (_error != null)
              ErrorView(message: _error!, onRetry: _loadPrograms)
            else if (_programs.isEmpty)
              _emptyPrograms()
            else
              ..._programs.map(_programRow),
          ],
        ),
      );

  Widget _programRow(DegreeProgram p) {
    final active = p.isActive;
    return Container(
      margin:  const EdgeInsets.only(bottom: 7),
      padding: const EdgeInsets.symmetric(
          horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color:        AppColors.surface,
        borderRadius: BorderRadius.circular(10),
        border:       Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  p.degreeName,
                  style: GoogleFonts.plusJakartaSans(
                    fontSize:   13,
                    fontWeight: FontWeight.w700,
                    color:      AppColors.text1,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  '${p.duration} · ${p.studyMode} · ${p.feeType} · ${p.status}',
                  style: GoogleFonts.plusJakartaSans(
                      fontSize: 11, color: AppColors.text3),
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(
                horizontal: 8, vertical: 3),
            decoration: BoxDecoration(
              color: active ? AppColors.mintPale : AppColors.surface,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                  color: active
                      ? AppColors.mint.withOpacity(.4)
                      : AppColors.border),
            ),
            child: Text(
              p.status,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   10,
                fontWeight: FontWeight.w600,
                color:      active
                    ? const Color(0xFF065F46)
                    : AppColors.text3,
              ),
            ),
          ),
          const SizedBox(width: 6),
          _iconBtn(
            icon:    Icons.edit_outlined,
            tooltip: 'Edit program',
            onTap: () async {
              final updated = await Navigator.push<bool>(
                context,
                MaterialPageRoute(
                  builder: (_) => ProgramFormScreen(
                    university: _university,
                    program:    p,
                  ),
                ),
              );
              if (updated == true) {
                _loadPrograms();
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Program updated successfully.',
                          style: GoogleFonts.plusJakartaSans()),
                      backgroundColor: AppColors.mint,
                    ),
                  );
                }
              }
            },
          ),
          const SizedBox(width: 4),
          if (active)
            _iconBtn(
              icon:    Icons.pause_circle_outline,
              tooltip: 'Deactivate',
              color:   AppColors.rose,
              onTap:   () => _deactivateProgram(p),
            ),
        ],
      ),
    );
  }

  Widget _emptyPrograms() => Padding(
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Center(
          child: Column(
            children: [
              const Icon(Icons.school_outlined,
                  size: 36, color: AppColors.text3),
              const SizedBox(height: 8),
              Text(
                'No programs added yet.',
                style: GoogleFonts.plusJakartaSans(
                    fontSize: 13, color: AppColors.text3),
              ),
            ],
          ),
        ),
      );

  Widget _card({required Widget child}) => Container(
        width: double.infinity,
        decoration: BoxDecoration(
          color:        AppColors.card,
          borderRadius: BorderRadius.circular(14),
          border:       Border.all(color: AppColors.border),
        ),
        padding: const EdgeInsets.all(18),
        child: child,
      );

  Widget _cardHeader(String title, {Widget? action}) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Row(
          children: [
            Text(
              title,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   10,
                fontWeight: FontWeight.w700,
                color:      AppColors.text3,
                letterSpacing: .5,
              ),
            ),
            const Spacer(),
            if (action != null) action,
          ],
        ),
      );

  Widget _infoRow(String key, String value,
      {bool highlight = false}) =>
      Padding(
        padding: const EdgeInsets.symmetric(vertical: 6),
        child: Row(
          children: [
            Text(
              key,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 12, color: AppColors.text3),
            ),
            const Spacer(),
            Text(
              value,
              style: GoogleFonts.plusJakartaSans(
                fontSize:   12,
                fontWeight: FontWeight.w600,
                color: highlight ? AppColors.sky : AppColors.text1,
              ),
            ),
          ],
        ),
      );

  Widget _iconBtn({
    required IconData      icon,
    required String        tooltip,
    required VoidCallback  onTap,
    Color                  color = AppColors.text3,
  }) =>
      Tooltip(
        message: tooltip,
        child: InkWell(
          onTap:        onTap,
          borderRadius: BorderRadius.circular(6),
          child: Container(
            width:  28,
            height: 28,
            decoration: BoxDecoration(
              border:       Border.all(color: AppColors.border),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Icon(icon, size: 14, color: color),
          ),
        ),
      );
}
