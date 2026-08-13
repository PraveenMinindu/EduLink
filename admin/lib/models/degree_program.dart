// =============================================================
// EduLink Admin — DegreeProgram model
// =============================================================

class DegreeProgram {
  final String  id;
  final String  universityId;
  final String  universityName;
  final String  degreeName;
  final String  faculty;
  final String  shortDescription;
  final String  fullDescription;
  final String  duration;
  final String  studyMode;
  final String  medium;
  final String  qualification;
  final String  entryRequirements;
  final String  feeType;
  final double  tuitionFee;
  final String  currency;
  final double  registrationFee;
  final bool    installmentAvailable;
  final String  campusName;
  final String  address;
  final double? latitude;
  final double? longitude;
  final String  nextIntake;
  final String  applicationStatus;
  final String  applicationDeadline;
  final String  phone;
  final String  email;
  final String  officialWebsite;
  final String  degreePageUrl;
  final String  applyNowUrl;
  final bool    ugcRecognized;
  final bool    ministryRecognized;
  final String  accreditation;
  final String  scholarships;
  final String  financialAid;
  final String  paymentPlans;
  final String  logoUrl;
  final String  campusImageUrl;
  final String  virtualTourUrl;
  final String  brochureUrl;
  final String  status;
  final String  createdBy;
  final String  updatedBy;

  const DegreeProgram({
    required this.id,
    required this.universityId,
    required this.universityName,
    required this.degreeName,
    required this.faculty,
    this.shortDescription    = '',
    this.fullDescription     = '',
    this.duration            = '',
    this.studyMode           = 'Full-time',
    this.medium              = 'English',
    this.qualification       = '',
    this.entryRequirements   = '',
    this.feeType             = 'Free',
    this.tuitionFee          = 0,
    this.currency            = 'LKR',
    this.registrationFee     = 0,
    this.installmentAvailable = false,
    this.campusName          = '',
    this.address             = '',
    this.latitude,
    this.longitude,
    this.nextIntake          = '',
    this.applicationStatus   = 'Coming Soon',
    this.applicationDeadline = '',
    this.phone               = '',
    this.email               = '',
    this.officialWebsite     = '',
    this.degreePageUrl       = '',
    this.applyNowUrl         = '',
    this.ugcRecognized       = false,
    this.ministryRecognized  = false,
    this.accreditation       = '',
    this.scholarships        = '',
    this.financialAid        = '',
    this.paymentPlans        = '',
    this.logoUrl             = '',
    this.campusImageUrl      = '',
    this.virtualTourUrl      = '',
    this.brochureUrl         = '',
    this.status              = 'Active',
    this.createdBy           = '',
    this.updatedBy           = '',
  });

  factory DegreeProgram.fromJson(Map<String, dynamic> j) => DegreeProgram(
        id:                   j['id']                   ?? '',
        universityId:         j['universityId']         ?? '',
        universityName:       j['universityName']       ?? '',
        degreeName:           j['degreeName']           ?? '',
        faculty:              j['faculty']              ?? '',
        shortDescription:     j['shortDescription']     ?? '',
        fullDescription:      j['fullDescription']      ?? '',
        duration:             j['duration']             ?? '',
        studyMode:            j['studyMode']            ?? 'Full-time',
        medium:               j['medium']               ?? 'English',
        qualification:        j['qualification']        ?? '',
        entryRequirements:    j['entryRequirements']    ?? '',
        feeType:              j['feeType']              ?? 'Free',
        tuitionFee:           (j['tuitionFee']          ?? 0).toDouble(),
        currency:             j['currency']             ?? 'LKR',
        registrationFee:      (j['registrationFee']     ?? 0).toDouble(),
        installmentAvailable: j['installmentAvailable'] ?? false,
        campusName:           j['campusName']           ?? '',
        address:              j['address']              ?? '',
        latitude:             j['latitude']  != null ? (j['latitude']  as num).toDouble() : null,
        longitude:            j['longitude'] != null ? (j['longitude'] as num).toDouble() : null,
        nextIntake:           j['nextIntake']           ?? '',
        applicationStatus:    j['applicationStatus']   ?? 'Coming Soon',
        applicationDeadline:  j['applicationDeadline'] ?? '',
        phone:                j['phone']                ?? '',
        email:                j['email']                ?? '',
        officialWebsite:      j['officialWebsite']      ?? '',
        degreePageUrl:        j['degreePageUrl']        ?? '',
        applyNowUrl:          j['applyNowUrl']          ?? '',
        ugcRecognized:        j['ugcRecognized']        ?? false,
        ministryRecognized:   j['ministryRecognized']  ?? false,
        accreditation:        j['accreditation']        ?? '',
        scholarships:         j['scholarships']         ?? '',
        financialAid:         j['financialAid']         ?? '',
        paymentPlans:         j['paymentPlans']         ?? '',
        logoUrl:              j['logoUrl']              ?? '',
        campusImageUrl:       j['campusImageUrl']       ?? '',
        virtualTourUrl:       j['virtualTourUrl']       ?? '',
        brochureUrl:          j['brochureUrl']          ?? '',
        status:               j['status']               ?? 'Active',
        createdBy:            j['createdBy']            ?? '',
        updatedBy:            j['updatedBy']            ?? '',
      );

  bool get isActive => status == 'Active';
  bool get isPaid   => feeType == 'Paid';
  bool get hasMap   => latitude != null && longitude != null;

  Map<String, dynamic> toJson() => {
        'id':                   id,
        'universityId':         universityId,
        'universityName':       universityName,
        'degreeName':           degreeName,
        'faculty':              faculty,
        'shortDescription':     shortDescription,
        'fullDescription':      fullDescription,
        'duration':             duration,
        'studyMode':            studyMode,
        'medium':               medium,
        'qualification':        qualification,
        'entryRequirements':    entryRequirements,
        'feeType':              feeType,
        'tuitionFee':           tuitionFee,
        'currency':             currency,
        'registrationFee':      registrationFee,
        'installmentAvailable': installmentAvailable,
        'campusName':           campusName,
        'address':              address,
        'latitude':             latitude,
        'longitude':            longitude,
        'nextIntake':           nextIntake,
        'applicationStatus':    applicationStatus,
        'applicationDeadline':  applicationDeadline,
        'phone':                phone,
        'email':                email,
        'officialWebsite':      officialWebsite,
        'degreePageUrl':        degreePageUrl,
        'applyNowUrl':          applyNowUrl,
        'ugcRecognized':        ugcRecognized,
        'ministryRecognized':   ministryRecognized,
        'accreditation':        accreditation,
        'scholarships':         scholarships,
        'financialAid':         financialAid,
        'paymentPlans':         paymentPlans,
        'logoUrl':              logoUrl,
        'campusImageUrl':       campusImageUrl,
        'virtualTourUrl':       virtualTourUrl,
        'brochureUrl':          brochureUrl,
        'status':               status,
        'createdBy':            createdBy,
        'updatedBy':            updatedBy,
      };
}
