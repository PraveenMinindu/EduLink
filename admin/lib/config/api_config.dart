class ApiConfig {
  static const String _localhost = 'http://localhost:8001';
  static const String _lanIp = 'http://10.116.164.69:8001';
  static const String _production = 'https://edulink-7i49.onrender.com';

  // Switch between _lanIp (local), _localhost (emulator), _production (Render)
  static const String baseUrl = _production;

  static const Duration defaultTimeout = Duration(seconds: 30);

  static const String login = '/admin/auth/login';
  static const String me = '/admin/auth/me';
  static const String stats = '/admin/dashboard/stats';
  static const String universities = '/admin/universities';
  static const String programs = '/admin/degree-programs';
}
