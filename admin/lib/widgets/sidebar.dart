// =============================================================
// EduLink Admin — Sidebar Widget
// Responsive: full on desktop, drawer on mobile
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/admin_user.dart';

// Fix 8: settings added to enum
enum AdminPage { dashboard, universities, settings }

class Sidebar extends StatelessWidget {
  final AdminPage            currentPage;
  final AdminUser?           admin;
  final ValueChanged<AdminPage> onNav;
  final VoidCallback         onSignOut;

  const Sidebar({
    super.key,
    required this.currentPage,
    required this.onNav,
    required this.onSignOut,
    this.admin,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 210,
      color: AppColors.sidebarBg,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ── Logo ─────────────────────────────────────────
          Container(
            color:   AppColors.navy,
            padding: const EdgeInsets.fromLTRB(18, 16, 18, 16),
            width:   double.infinity,
            child: Row(
              children: [
                Text(
                  'Edu',
                  style: GoogleFonts.plusJakartaSans(
                    fontSize:   18,
                    fontWeight: FontWeight.w700,
                    color:      Colors.white,
                  ),
                ),
                Text(
                  'Link',
                  style: GoogleFonts.plusJakartaSans(
                    fontSize:   18,
                    fontWeight: FontWeight.w300,
                    color:      AppColors.sidebarTextOn,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color:        AppColors.navy3,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    'Admin',
                    style: GoogleFonts.plusJakartaSans(
                      fontSize:   10,
                      fontWeight: FontWeight.w600,
                      color:      AppColors.sidebarTextOn,
                    ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 12),
          _label('MAIN'),
          _navItem(
            icon:  Icons.dashboard_outlined,
            label: 'Dashboard',
            page:  AdminPage.dashboard,
          ),
          _navItem(
            icon:  Icons.account_balance_outlined,
            label: 'Universities',
            page:  AdminPage.universities,
          ),
          const SizedBox(height: 4),

          // Fix 8: Settings nav item
          _navItem(
            icon:  Icons.settings_outlined,
            label: 'Settings',
            page:  AdminPage.settings,
          ),

          const Spacer(),

          // ── Admin info ────────────────────────────────────
          if (admin != null)
            Container(
              margin:  const EdgeInsets.all(12),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color:        Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                    color: Colors.white.withOpacity(0.08)),
              ),
              child: Row(
                children: [
                  CircleAvatar(
                    radius:          16,
                    backgroundColor: AppColors.navy3,
                    child: Text(
                      _initials(admin!.name),
                      style: GoogleFonts.plusJakartaSans(
                        fontSize:   11,
                        fontWeight: FontWeight.w700,
                        color:      AppColors.sidebarTextOn,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          admin!.name,
                          style: GoogleFonts.plusJakartaSans(
                            fontSize:   12,
                            fontWeight: FontWeight.w600,
                            color:      Colors.white,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        Text(
                          admin!.role,
                          style: GoogleFonts.plusJakartaSans(
                            fontSize: 10,
                            color:    AppColors.sidebarText,
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    icon:        const Icon(Icons.logout,
                        size: 16, color: AppColors.sidebarText),
                    tooltip:     'Sign out',
                    onPressed:   onSignOut,
                    padding:     EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                ],
              ),
            ),
          const SizedBox(height: 8),
        ],
      ),
    );
  }

  Widget _label(String text) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
        child: Text(
          text,
          style: GoogleFonts.plusJakartaSans(
            fontSize:   10,
            fontWeight: FontWeight.w700,
            color:      AppColors.sidebarText,
            letterSpacing: 1,
          ),
        ),
      );

  Widget _navItem({
    required IconData   icon,
    required String     label,
    required AdminPage  page,
  }) {
    final active = currentPage == page;
    return Container(
      decoration: BoxDecoration(
        color: active
            ? AppColors.sky.withOpacity(0.18)
            : Colors.transparent,
        border: Border(
          right: BorderSide(
            color: active ? AppColors.sky : Colors.transparent,
            width: 2,
          ),
        ),
      ),
      child: ListTile(
        dense: true,
        leading: Icon(
          icon,
          size:  18,
          color: active ? Colors.white : AppColors.sidebarText,
        ),
        title: Text(
          label,
          style: GoogleFonts.plusJakartaSans(
            fontSize:   13,
            fontWeight: active ? FontWeight.w600 : FontWeight.w500,
            color:      active ? Colors.white : AppColors.sidebarText,
          ),
        ),
        onTap: () => onNav(page),
      ),
    );
  }

  String _initials(String name) {
    final parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return '${parts.first[0]}${parts.last[0]}'.toUpperCase();
    }
    return name.isNotEmpty ? name[0].toUpperCase() : 'A';
  }
}
