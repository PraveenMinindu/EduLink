class StudentModel {
  final String studentId;
  final String name;
  final int age;
  final String grade;
  final String stream;
  final String school;
  final String district;

  StudentModel({
    required this.studentId,
    required this.name,
    required this.age,
    required this.grade,
    required this.stream,
    required this.school,
    required this.district,
  });

  Map<String, dynamic> toJson() => {
    'student_id': studentId,
    'name': name,
    'age': age,
    'grade': grade,
    'stream': stream,
    'school': school,
    'district': district,
  };
}
