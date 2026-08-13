// =============================================================
// EduLink Admin — University Add/Edit Form
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/university.dart';
import '../services/api_service.dart';

class UniversityFormScreen extends StatefulWidget {
  final University? university; // null = create, non-null = edit
  const UniversityFormScreen({super.key, this.university});

  @override
  State<UniversityFormScreen> createState() => _UniversityFormScreenState();
}

class _UniversityFormScreenState extends State<UniversityFormScreen> {
  final _nameCtrl     = TextEditingController();
  final _locationCtrl = TextEditingController();
  final _websiteCtrl  = TextEditingController();
  final _shortCtrl    = TextEditingController();
  final _fullCtrl     = TextEditingController();
  final _logoCtrl     = TextEditingController();

  String _type   = 'State';
  String _status = 'Active';
  bool   _loading = false;
  String? _error;

  bool get _isEdit => widget.university != null;

  @override
  void initState() {
    super.initState();
    if (_isEdit) {
      final u         = widget.university!;
      _nameCtrl.text  = u.name;
      _locationCtrl.text = u.location;
      _websiteCtrl.text  = u.website;
      _shortCtrl.text    = u.shortDescription;
      _fullCtrl.text     = u.fullDescription;
      _logoCtrl.text     = u.logoUrl;
      // Fix: assigning the raw Firestore value straight into a dropdown's
      // value crashes (DropdownButton assertion) if it doesn't exactly
      // match one of the options — e.g. different casing from a bulk
      // import. Match case-insensitively and fall back to the first
      // option instead of crashing the edit screen.
      _type              = _matchOption(u.type, const ['State', 'Private']);
      _status            = _matchOption(u.status, const ['Active', 'Inactive']);
    }
  }

  static String _matchOption(String value, List<String> options) {
    for (final o in options) {
      if (o.toLowerCase() == value.trim().toLowerCase()) return o;
    }
    return options.first;
  }

  Future<void> _save() async {
    final name     = _nameCtrl.text.trim();
    final location = _locationCtrl.text.trim();

    if (name.length < 3) {
      setState(() => _error = 'University name must be at least 3 characters.');
      return;
    }
    if (location.isEmpty) {
      setState(() => _error = 'Location is required.');
      return;
    }

    setState(() { _loading = true; _error = null; });

    final data = {
      'name':             name,
      'type':             _type,
      'location':         location,
      'website':          _websiteCtrl.text.trim(),
      'shortDescription': _shortCtrl.text.trim(),
      'fullDescription':  _fullCtrl.text.trim(),
      'logoUrl':          _logoCtrl.text.trim(),
      'status':           _status,
    };

    try {
      if (_isEdit) {
        await ApiService.updateUniversity(widget.university!.id, data);
      } else {
        await ApiService.createUniversity(data);
      }
      if (mounted) Navigator.pop(context, true);
    } catch (e) {
      setState(() {
        _error   = e.toString().replaceFirst('Exception: ', '');
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        foregroundColor: Colors.white,
        title: Text(
          _isEdit ? 'Edit university' : 'Add university',
          style: GoogleFonts.plusJakartaSans(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: Colors.white),
        ),
        actions: [
          if (_loading)
            const Padding(
              padding: EdgeInsets.all(14),
              child: SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                      color: Colors.white, strokeWidth: 2)),
            )
          else
            TextButton(
              onPressed: _save,
              child: Text(
                _isEdit ? 'Save changes' : 'Save university',
                style: GoogleFonts.plusJakartaSans(
                    color: Colors.white,
                    fontWeight: FontWeight.w600),
              ),
            ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          // Fix: a fixed width:700 Container overflowed horizontally on
          // phones/small windows narrower than 700. A max-width constraint
          // with width:double.infinity fills the available space up to
          // 700 and shrinks below that.
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 700),
            child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color:        AppColors.card,
              borderRadius: BorderRadius.circular(16),
              border:       Border.all(color: AppColors.border),
            ),
            padding: const EdgeInsets.all(28),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (_error != null) ...[
                  _errorBanner(),
                  const SizedBox(height: 16),
                ],

                _sectionLabel('Basic information'),
                const SizedBox(height: 12),
                _field('University name *', _nameCtrl,
                    hint: 'University of Moratuwa'),
                const SizedBox(height: 12),
                _row2(
                  _dropdownField(
                    label:   'Type *',
                    value:   _type,
                    options: const ['State', 'Private'],
                    onChanged: (v) => setState(() => _type = v!),
                  ),
                  _dropdownField(
                    label:    'Status',
                    value:    _status,
                    options:  const ['Active', 'Inactive'],
                    onChanged: (v) => setState(() => _status = v!),
                  ),
                ),
                const SizedBox(height: 12),
                _field('Location *', _locationCtrl,
                    hint: 'Moratuwa, Western Province'),
                const SizedBox(height: 12),
                _field('Official website', _websiteCtrl,
                    hint: 'https://uom.lk'),
                const SizedBox(height: 20),

                _sectionLabel('Description'),
                const SizedBox(height: 12),
                _field('Short description', _shortCtrl,
                    hint:     'Brief one-line description',
                    maxLines: 2),
                const SizedBox(height: 12),
                _field('Full description', _fullCtrl,
                    hint:     'Detailed description of the university',
                    maxLines: 5),
                const SizedBox(height: 20),

                _sectionLabel('Resources'),
                const SizedBox(height: 12),
                _field('Logo URL', _logoCtrl,
                    hint: 'https://... (publicly accessible image URL)'),

                const SizedBox(height: 28),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    OutlinedButton(
                      onPressed: () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        foregroundColor:  AppColors.text2,
                        side: const BorderSide(color: AppColors.border),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 20, vertical: 13),
                      ),
                      child: Text('Cancel',
                          style: GoogleFonts.plusJakartaSans(
                              fontWeight: FontWeight.w500)),
                    ),
                    const SizedBox(width: 12),
                    ElevatedButton(
                      onPressed: _loading ? null : _save,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.sky,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 24, vertical: 13),
                      ),
                      child: Text(
                        _isEdit ? 'Save changes' : 'Save university',
                        style: GoogleFonts.plusJakartaSans(
                            fontWeight: FontWeight.w600),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _sectionLabel(String text) => Text(
        text,
        style: GoogleFonts.plusJakartaSans(
          fontSize: 10,
          fontWeight: FontWeight.w700,
          color: AppColors.text3,
          letterSpacing: .5,
        ),
      );

  // Fix: two side-by-side fields were cramped/unusable on narrow phones —
  // stack them vertically below 380px instead of forcing a Row.
  Widget _row2(Widget a, Widget b) => LayoutBuilder(
        builder: (ctx, c) {
          if (c.maxWidth < 380) {
            return Column(children: [a, const SizedBox(height: 12), b]);
          }
          return Row(children: [
            Expanded(child: a),
            const SizedBox(width: 12),
            Expanded(child: b),
          ]);
        },
      );

  Widget _field(
    String label,
    TextEditingController ctrl, {
    String hint      = '',
    int maxLines     = 1,
  }) =>
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: AppColors.text3,
                  letterSpacing: .4)),
          const SizedBox(height: 5),
          TextField(
            controller: ctrl,
            maxLines:   maxLines,
            style: GoogleFonts.plusJakartaSans(
                fontSize: 13, color: AppColors.text1),
            decoration: InputDecoration(
              hintText:  hint,
              hintStyle: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text3),
              filled:    true,
              fillColor: AppColors.surface,
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
              contentPadding: const EdgeInsets.symmetric(
                  horizontal: 12, vertical: 10),
            ),
          ),
        ],
      );

  Widget _dropdownField({
    required String label,
    required String value,
    required List<String> options,
    required ValueChanged<String?> onChanged,
  }) =>
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: AppColors.text3,
                  letterSpacing: .4)),
          const SizedBox(height: 5),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 12),
            decoration: BoxDecoration(
              color:        AppColors.surface,
              borderRadius: BorderRadius.circular(10),
              border:       Border.all(color: AppColors.border),
            ),
            child: DropdownButton<String>(
              // Defensive: DropdownButton asserts if value isn't exactly
              // one of items — never let an unexpected value crash this.
              value:         options.contains(value) ? value : null,
              hint:          Text(value, style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1)),
              isExpanded:    true,
              underline:     const SizedBox(),
              style: GoogleFonts.plusJakartaSans(
                  fontSize: 13, color: AppColors.text1),
              items: options
                  .map((o) =>
                      DropdownMenuItem(value: o, child: Text(o)))
                  .toList(),
              onChanged: onChanged,
            ),
          ),
        ],
      );

  Widget _errorBanner() => Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color:        AppColors.rosePale,
          borderRadius: BorderRadius.circular(10),
          border:
              Border.all(color: AppColors.rose.withOpacity(.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.error_outline,
                color: AppColors.rose, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(_error!,
                  style: GoogleFonts.plusJakartaSans(
                      fontSize: 13, color: AppColors.rose)),
            ),
          ],
        ),
      );

  @override
  void dispose() {
    _nameCtrl.dispose();
    _locationCtrl.dispose();
    _websiteCtrl.dispose();
    _shortCtrl.dispose();
    _fullCtrl.dispose();
    _logoCtrl.dispose();
    super.dispose();
  }
}
