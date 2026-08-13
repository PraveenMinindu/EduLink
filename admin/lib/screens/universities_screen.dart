// =============================================================
// EduLink Admin — Universities List Screen
// Fix 11: ErrorView widget used instead of inline error card
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/university.dart';
import '../services/api_service.dart';
import '../widgets/error_view.dart';
import 'university_detail_screen.dart';
import 'university_form_screen.dart';

class UniversitiesScreen extends StatefulWidget {
  const UniversitiesScreen({super.key});

  @override
  State<UniversitiesScreen> createState() => _UniversitiesScreenState();
}

class _UniversitiesScreenState extends State<UniversitiesScreen> {
  List<University> _all      = [];
  List<University> _filtered = [];
  bool    _loading = true;
  String? _error;
  String  _search  = '';
  String  _status  = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; });
    try {
      final list = await ApiService.getUniversities(
        status: _status.isEmpty ? null : _status,
      );
      setState(() { _all = list; _loading = false; });
      _applyFilter();
    } catch (e) {
      setState(() {
        _error   = e.toString().replaceFirst('Exception: ', '');
        _loading = false;
      });
    }
  }

  void _applyFilter() {
    setState(() {
      _filtered = _all.where((u) {
        if (_search.isEmpty) return true;
        final q = _search.toLowerCase();
        return u.name.toLowerCase().contains(q) ||
               u.location.toLowerCase().contains(q);
      }).toList();
    });
  }

  Future<void> _delete(University u) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: Text(
          'Delete university',
          style: GoogleFonts.plusJakartaSans(
              fontWeight: FontWeight.w700),
        ),
        content: Text(
          'Are you sure you want to delete "${u.name}"?\n\n'
          'This action cannot be undone.',
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
              foregroundColor: Colors.white,
            ),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (ok != true) return;
    try {
      await ApiService.deleteUniversity(u.id);
      _load();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              '"${u.name}" deleted.',
              style: GoogleFonts.plusJakartaSans(),
            ),
            backgroundColor: AppColors.mint,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              e.toString().replaceFirst('Exception: ', ''),
              style: GoogleFonts.plusJakartaSans(),
            ),
            backgroundColor: AppColors.rose,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Universities',
                      style: GoogleFonts.plusJakartaSans(
                        fontSize:   22,
                        fontWeight: FontWeight.w700,
                        color:      AppColors.text1,
                      ),
                    ),
                    Text(
                      '${_filtered.length} institution(s)',
                      style: GoogleFonts.plusJakartaSans(
                          fontSize: 13, color: AppColors.text3),
                    ),
                  ],
                ),
              ),
              // Fix: Add university button fully wired
              ElevatedButton.icon(
                onPressed: () async {
                  final created = await Navigator.push<bool>(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const UniversityFormScreen(),
                    ),
                  );
                  if (created == true) {
                    _load();
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('University created successfully.',
                              style: GoogleFonts.plusJakartaSans()),
                          backgroundColor: AppColors.mint,
                        ),
                      );
                    }
                  }
                },
                icon:  const Icon(Icons.add, size: 16),
                label: const Text('Add university'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.sky,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                      horizontal: 16, vertical: 12),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                  textStyle: GoogleFonts.plusJakartaSans(
                      fontSize: 13, fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Search + filter bar
          Row(
            children: [
              Expanded(
                child: TextField(
                  onChanged: (v) {
                    _search = v;
                    _applyFilter();
                  },
                  decoration: InputDecoration(
                    hintText:  'Search by name or location…',
                    hintStyle: GoogleFonts.plusJakartaSans(
                        fontSize: 13, color: AppColors.text3),
                    prefixIcon: const Icon(Icons.search,
                        color: AppColors.text3, size: 18),
                    filled:     true,
                    fillColor:  AppColors.card,
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide:
                            const BorderSide(color: AppColors.border)),
                    enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide:
                            const BorderSide(color: AppColors.border)),
                    focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide: const BorderSide(
                            color: AppColors.sky, width: 1.5)),
                    contentPadding:
                        const EdgeInsets.symmetric(vertical: 10),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              _dropdown(
                value:  _status,
                items:  const ['', 'Active', 'Inactive'],
                labels: const ['All status', 'Active', 'Inactive'],
                onChanged: (v) {
                  _status = v ?? '';
                  _load();
                },
              ),
            ],
          ),
          const SizedBox(height: 16),

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
          else if (_filtered.isEmpty)
            _emptyState()
          else
            // Fix: the 4-column table was cramped/unreadable on phones —
            // switch to a stacked card layout below 700px.
            LayoutBuilder(
              builder: (ctx, c) =>
                  c.maxWidth < 700 ? _cardList() : _table(),
            ),
        ],
      ),
    );
  }

  Widget _table() => Container(
        decoration: BoxDecoration(
          color:        AppColors.card,
          borderRadius: BorderRadius.circular(14),
          border:       Border.all(color: AppColors.border),
        ),
        child: Column(
          children: [
            // Header row
            Container(
              padding: const EdgeInsets.symmetric(
                  horizontal: 16, vertical: 10),
              decoration: const BoxDecoration(
                border: Border(
                    bottom: BorderSide(color: AppColors.surface)),
              ),
              child: Row(
                children: [
                  Expanded(flex: 3, child: _th('University')),
                  Expanded(child: _th('Type')),
                  Expanded(child: _th('Status')),
                  const SizedBox(width: 80),
                ],
              ),
            ),
            ..._filtered.asMap().entries.map((e) {
              final i = e.key;
              final u = e.value;
              return _row(u, i == _filtered.length - 1);
            }),
          ],
        ),
      );

  // Fix: stacked-card layout used on narrow screens instead of the table.
  Widget _cardList() => Column(
        children: _filtered
            .map((u) => Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  decoration: BoxDecoration(
                    color:        AppColors.card,
                    borderRadius: BorderRadius.circular(14),
                    border:       Border.all(color: AppColors.border),
                  ),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () async {
                      await Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                              UniversityDetailScreen(university: u),
                        ),
                      );
                      _load();
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(14),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      u.name,
                                      style: GoogleFonts.plusJakartaSans(
                                        fontSize:   13,
                                        fontWeight: FontWeight.w700,
                                        color:      AppColors.text1,
                                      ),
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      u.location,
                                      style: GoogleFonts.plusJakartaSans(
                                          fontSize: 11,
                                          color: AppColors.text3),
                                    ),
                                  ],
                                ),
                              ),
                              _iconBtn(
                                icon:    Icons.edit_outlined,
                                tooltip: 'Edit',
                                onTap: () async {
                                  final updated =
                                      await Navigator.push<bool>(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) =>
                                          UniversityFormScreen(
                                              university: u),
                                    ),
                                  );
                                  if (updated == true) {
                                    _load();
                                    if (mounted) {
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        SnackBar(
                                          content: Text(
                                              'University updated successfully.',
                                              style: GoogleFonts
                                                  .plusJakartaSans()),
                                          backgroundColor: AppColors.mint,
                                        ),
                                      );
                                    }
                                  }
                                },
                              ),
                              const SizedBox(width: 4),
                              _iconBtn(
                                icon:    Icons.delete_outline,
                                tooltip: 'Delete',
                                color:   AppColors.rose,
                                onTap:   () => _delete(u),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Row(
                            children: [
                              _badge(
                                u.type,
                                u.type == 'State'
                                    ? AppColors.skyPale
                                    : AppColors.violetPale,
                                u.type == 'State'
                                    ? const Color(0xFF1D4ED8)
                                    : const Color(0xFF5B21B6),
                              ),
                              const SizedBox(width: 6),
                              _badge(
                                u.status,
                                u.isActive
                                    ? AppColors.mintPale
                                    : AppColors.surface,
                                u.isActive
                                    ? const Color(0xFF065F46)
                                    : AppColors.text3,
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ))
            .toList(),
      );

  Widget _row(University u, bool last) => InkWell(
        onTap: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => UniversityDetailScreen(university: u),
            ),
          );
          _load();
        },
        child: Container(
          decoration: BoxDecoration(
            border: last
                ? null
                : const Border(
                    bottom: BorderSide(color: AppColors.surface)),
          ),
          padding: const EdgeInsets.symmetric(
              horizontal: 16, vertical: 14),
          child: Row(
            children: [
              Expanded(
                flex: 3,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      u.name,
                      style: GoogleFonts.plusJakartaSans(
                        fontSize:   13,
                        fontWeight: FontWeight.w700,
                        color:      AppColors.text1,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      u.location,
                      style: GoogleFonts.plusJakartaSans(
                          fontSize: 11, color: AppColors.text3),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: _badge(
                  u.type,
                  u.type == 'State'
                      ? AppColors.skyPale
                      : AppColors.violetPale,
                  u.type == 'State'
                      ? const Color(0xFF1D4ED8)
                      : const Color(0xFF5B21B6),
                ),
              ),
              Expanded(
                child: _badge(
                  u.status,
                  u.isActive ? AppColors.mintPale : AppColors.surface,
                  u.isActive
                      ? const Color(0xFF065F46)
                      : AppColors.text3,
                ),
              ),
              SizedBox(
                width: 80,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    _iconBtn(
                      icon:    Icons.edit_outlined,
                      tooltip: 'Edit',
                      onTap: () async {
                        final updated = await Navigator.push<bool>(
                          context,
                          MaterialPageRoute(
                            builder: (_) =>
                                UniversityFormScreen(university: u),
                          ),
                        );
                        if (updated == true) {
                          _load();
                          if (mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('University updated successfully.',
                                    style: GoogleFonts.plusJakartaSans()),
                                backgroundColor: AppColors.mint,
                              ),
                            );
                          }
                        }
                      },
                    ),
                    const SizedBox(width: 4),
                    _iconBtn(
                      icon:    Icons.delete_outline,
                      tooltip: 'Delete',
                      color:   AppColors.rose,
                      onTap:   () => _delete(u),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );

  Widget _th(String t) => Text(
        t,
        style: GoogleFonts.plusJakartaSans(
          fontSize:   10,
          fontWeight: FontWeight.w700,
          color:      AppColors.text3,
          letterSpacing: .4,
        ),
      );

  Widget _badge(String label, Color bg, Color fg) => Container(
        padding: const EdgeInsets.symmetric(
            horizontal: 10, vertical: 3),
        decoration: BoxDecoration(
            color: bg, borderRadius: BorderRadius.circular(20)),
        child: Text(
          label,
          style: GoogleFonts.plusJakartaSans(
            fontSize:   11,
            fontWeight: FontWeight.w600,
            color:      fg,
          ),
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

  Widget _dropdown({
    required String              value,
    required List<String>        items,
    required List<String>        labels,
    required ValueChanged<String?> onChanged,
  }) =>
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 12),
        decoration: BoxDecoration(
          color:        AppColors.card,
          borderRadius: BorderRadius.circular(10),
          border:       Border.all(color: AppColors.border),
        ),
        child: DropdownButton<String>(
          value:     value,
          underline: const SizedBox(),
          style: GoogleFonts.plusJakartaSans(
              fontSize: 13, color: AppColors.text2),
          items: items.asMap().entries.map((e) {
            return DropdownMenuItem(
                value: e.value,
                child: Text(labels[e.key]));
          }).toList(),
          onChanged: onChanged,
        ),
      );

  Widget _emptyState() => Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 48),
          child: Column(
            children: [
              const Icon(Icons.account_balance_outlined,
                  size: 48, color: AppColors.text3),
              const SizedBox(height: 12),
              Text(
                'No universities yet.',
                style: GoogleFonts.plusJakartaSans(
                  fontSize:   15,
                  fontWeight: FontWeight.w600,
                  color:      AppColors.text2,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                'Add the first university to get started.',
                style: GoogleFonts.plusJakartaSans(
                    fontSize: 13, color: AppColors.text3),
              ),
            ],
          ),
        ),
      );
}
