// =============================================================
// EduLink Admin — AdminUser model
// =============================================================

class AdminUser {
  final String uid;
  final String name;
  final String email;
  final String role;
  final String? lastLogin; // ISO 8601 string, null if never logged in before

  const AdminUser({
    required this.uid,
    required this.name,
    required this.email,
    this.role = 'admin',
    this.lastLogin,
  });

  factory AdminUser.fromJson(Map<String, dynamic> j) => AdminUser(
    uid: j['uid'] ?? '',
    name: j['name'] ?? '',
    email: j['email'] ?? '',
    role: j['role'] ?? 'admin',
    lastLogin: j['lastLogin'] as String?,
  );

  Map<String, dynamic> toJson() => {
    'uid': uid,
    'name': name,
    'email': email,
    'role': role,
    'lastLogin': lastLogin,
  };
}
