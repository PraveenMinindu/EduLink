// =============================================================
// EduLink Admin — Admin Scaffold
// Responsive layout: sidebar + top bar + main content
// Desktop >900px: sidebar visible
// Mobile  <900px: hamburger drawer
// =============================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../config/app_colors.dart';
import '../models/admin_user.dart';
import 'sidebar.dart';

class AdminScaffold extends StatelessWidget {
  final AdminPage currentPage;
  final AdminUser? admin;
  final Widget child;
  final ValueChanged<AdminPage> onNav;
  final VoidCallback onSignOut;

  const AdminScaffold({
    super.key,
    required this.currentPage,
    required this.child,
    required this.onNav,
    required this.onSignOut,
    this.admin,
  });

  @override
  Widget build(BuildContext context) {
    final width     = MediaQuery.of(context).size.width;
    final isDesktop = width > 900;

    if (isDesktop) {
      return Scaffold(
        backgroundColor: AppColors.surface,
        body: Row(
          children: [
            Sidebar(
              currentPage: currentPage,
              admin:       admin,
              onNav:       onNav,
              onSignOut:   onSignOut,
            ),
            Expanded(
              child: Column(
                children: [
                  _TopBar(admin: admin, onSignOut: onSignOut),
                  Expanded(child: child),
                ],
              ),
            ),
          ],
        ),
      );
    }

    // Mobile — drawer
    return Scaffold(
      backgroundColor: AppColors.surface,
      drawer: Drawer(
        backgroundColor: AppColors.sidebarBg,
        child: Sidebar(
          currentPage: currentPage,
          admin:       admin,
          onNav:       (p) {
            Navigator.pop(context);
            onNav(p);
          },
          onSignOut:   onSignOut,
        ),
      ),
      appBar: AppBar(
        backgroundColor: AppColors.navy,
        iconTheme: const IconThemeData(color: Colors.white),
        title: Text(
          'EduLink Admin',
          style: GoogleFonts.plusJakartaSans(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            color: Colors.white,
          ),
        ),
        actions: [
          if (admin != null)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: CircleAvatar(
                radius: 14,
                backgroundColor: AppColors.navy3,
                child: Text(
                  _initials(admin!.name),
                  style: const TextStyle(
                      fontSize: 10, color: Colors.white),
                ),
              ),
            ),
        ],
      ),
      body: child,
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

class _TopBar extends StatelessWidget {
  final AdminUser? admin;
  final VoidCallback onSignOut;

  const _TopBar({this.admin, required this.onSignOut});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 52,
      color: AppColors.navy,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Row(
        children: [
          const Spacer(),
          if (admin != null) ...[
            Container(
              padding: const EdgeInsets.symmetric(
                  horizontal: 10, vertical: 3),
              decoration: BoxDecoration(
                color: AppColors.navy3,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                'Admin panel',
                style: GoogleFonts.plusJakartaSans(
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                  color: AppColors.sidebarTextOn,
                ),
              ),
            ),
            const SizedBox(width: 10),
            CircleAvatar(
              radius: 14,
              backgroundColor: AppColors.navy3,
              child: Text(
                _initials(admin!.name),
                style: GoogleFonts.plusJakartaSans(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: AppColors.sidebarTextOn,
                ),
              ),
            ),
          ],
        ],
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
