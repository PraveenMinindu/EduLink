// =============================================================
// EduLink Admin Panel — Main entry point
// Flutter Web application
// Firebase initialized via FlutterFire (firebase_options.dart)
// Run: flutterfire configure  to generate firebase_options.dart
// =============================================================

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_fonts/google_fonts.dart';
import 'firebase_options.dart';
import 'config/app_colors.dart';
import 'models/admin_user.dart';
import 'services/auth_service.dart';
import 'services/api_service.dart';
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/universities_screen.dart';
import 'screens/settings_screen.dart';
import 'widgets/admin_scaffold.dart';
import 'widgets/sidebar.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  runApp(const EduLinkAdminApp());
}

class EduLinkAdminApp extends StatelessWidget {
  const EduLinkAdminApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EduLink Admin',
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.light,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.sky),
        textTheme: GoogleFonts.plusJakartaSansTextTheme(),
        useMaterial3: true,
        scaffoldBackgroundColor: AppColors.surface,
      ),
      home: const _AppRoot(),
    );
  }
}

class _AppRoot extends StatefulWidget {
  const _AppRoot();

  @override
  State<_AppRoot> createState() => _AppRootState();
}

class _AppRootState extends State<_AppRoot> {
  AdminUser? _admin;
  AdminPage _page = AdminPage.dashboard;
  bool _checking = true;
  StreamSubscription? _authSub;

  @override
  void initState() {
    super.initState();
    ApiService.onSessionExpired = _handleSessionExpired;
    _authSub = FirebaseAuth.instance.authStateChanges().listen(
      _onAuthStateChanged,
    );
  }

  Future<void> _onAuthStateChanged(User? user) async {
    if (user == null) {
      if (!mounted) return;
      setState(() {
        _admin = null;
        _checking = false;
      });
      return;
    }
    try {
      final me = await AuthService.getMe();
      if (!mounted) return;
      setState(() {
        _admin = me;
        _checking = false;
      });
    } catch (e) {
      debugPrint('getMe() failed: $e');
      await AuthService.signOut();
      if (!mounted) return;
      setState(() {
        _admin = null;
        _checking = false;
      });
    }
  }

  Future<void> _handleSessionExpired() async {
    await AuthService.signOut();

    if (!mounted) return;

    setState(() {
      _admin = null;
      _page = AdminPage.dashboard;
      _checking = false;
    });
  }

  @override
  void dispose() {
    _authSub?.cancel();
    super.dispose();
  }

  Future<void> _signOut() async {
    await AuthService.signOut();
    if (!mounted) return;
    setState(() {
      _admin = null;
      _page = AdminPage.dashboard;
      _checking = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_checking) {
      return const Scaffold(
        backgroundColor: AppColors.navy,
        body: Center(child: CircularProgressIndicator(color: Colors.white)),
      );
    }

    if (_admin == null) {
      return LoginScreen(
        onLogin: (admin) {
          setState(() {
            _admin = admin;
            _page = AdminPage.dashboard;
          });
        },
      );
    }

    return AdminScaffold(
      currentPage: _page,
      admin: _admin,
      onNav: (p) => setState(() => _page = p),
      onSignOut: _signOut,
      child: _buildPage(),
    );
  }

  Widget _buildPage() {
    switch (_page) {
      case AdminPage.dashboard:
        return const DashboardScreen();
      case AdminPage.universities:
        return const UniversitiesScreen();
      case AdminPage.settings:
        return SettingsScreen(
          admin: _admin!,
          onAdminUpdated: (u) => setState(() => _admin = u),
        );
    }
  }
}
