class ApiConfig {
  static const String _localhost = 'http://localhost:8001';
  static const String _lanIp = 'http://10.116.164.69:8001';

  // Change _lanIp to _localhost when running on emulator
  static const String baseUrl = _lanIp;

  static const Duration defaultTimeout = Duration(seconds: 30);

  static const String login = '/admin/auth/login';
  static const String me = '/admin/auth/me';
  static const String stats = '/admin/dashboard/stats';
  static const String universities = '/admin/universities';
  static const String programs = '/admin/degree-programs';
}
