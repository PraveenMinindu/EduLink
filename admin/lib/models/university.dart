// =============================================================
// EduLink Admin — University model
// =============================================================

class University {
  final String id;
  final String name;
  final String type;
  final String location;
  final String website;
  final String shortDescription;
  final String fullDescription;
  final String logoUrl;
  final String status;
  final String createdBy;
  final String updatedBy;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const University({
    required this.id,
    required this.name,
    required this.type,
    required this.location,
    this.website = '',
    this.shortDescription = '',
    this.fullDescription = '',
    this.logoUrl = '',
    this.status = 'Active',
    this.createdBy = '',
    this.updatedBy = '',
    this.createdAt,
    this.updatedAt,
  });

  factory University.fromJson(Map<String, dynamic> j) => University(
    id: j['id'] ?? '',
    name: j['name'] ?? '',
    type: j['type'] ?? '',
    location: j['location'] ?? '',
    website: j['website'] ?? '',
    shortDescription: j['shortDescription'] ?? '',
    fullDescription: j['fullDescription'] ?? '',
    logoUrl: j['logoUrl'] ?? '',
    status: j['status'] ?? 'Active',
    createdBy: j['createdBy'] ?? '',
    updatedBy: j['updatedBy'] ?? '',
    createdAt: DateTime.tryParse(j['createdAt'] ?? ''),
    updatedAt: DateTime.tryParse(j['updatedAt'] ?? ''),
  );

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'type': type,
    'location': location,
    'website': website,
    'shortDescription': shortDescription,
    'fullDescription': fullDescription,
    'logoUrl': logoUrl,
    'status': status,
    'createdBy': createdBy,
    'updatedBy': updatedBy,
    'createdAt': createdAt?.toIso8601String(),
    'updatedAt': updatedAt?.toIso8601String(),
  };

  bool get isActive => status == 'Active';
}
