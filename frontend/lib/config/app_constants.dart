class AppConstants {
  // API
  static const String baseUrl = "http://10.75.67.69:8001";
  // For physical device use your computer's IP:
  // static const String baseUrl = "http://192.168.1.xxx:8000";

  // MCQ
  static const int totalQuestions = 40;

  static const List<String> sections = [
    "Section 1 — Personality & Cognitive Style",
    "Section 2 — Skills & Capability Assessment",
    "Section 3 — Interests & Motivation",
    "Section 4 — Career Orientation & Future Vision",
  ];

  static const List<String> questions = [
    "I enjoy analysing complex situations before taking action.",
    "I feel comfortable solving problems that have no clear answer.",
    "I enjoy identifying patterns in information or behaviour.",
    "I prefer logical explanations over emotional reasoning.",
    "I often generate creative solutions to challenges.",
    "I enjoy writing or explaining how things work step by step.",
    "I pay close attention to details others may overlook.",
    "I think about how future trends may affect current decisions.",
    "I adapt easily to changing environments.",
    "I enjoy working closely with other people to solve problems.",
    "I can interpret graphs or data visualisations.",
    "I feel comfortable using digital tools to solve problems.",
    "I can explain complex ideas in simple language.",
    "I can identify inefficiencies in a workflow.",
    "I feel confident managing small projects.",
    "I can analyse information before making decisions.",
    "I can present ideas clearly to an audience.",
    "I enjoy working with numbers, data, or statistics.",
    "I can evaluate risks and benefits objectively.",
    "I can think strategically when planning projects.",
    "I prefer designing or building things over analysing or reporting them.",
    "I feel excited about future technologies.",
    "I enjoy solving problems related to business or economics.",
    "I prefer creative challenges over repetitive tasks.",
    "I enjoy analysing how markets or systems evolve.",
    "I enjoy learning about entrepreneurship.",
    "I feel motivated when solving real-world problems.",
    "I enjoy exploring data to discover insights.",
    "I am motivated by intellectual challenges.",
    "I enjoy combining technology with creativity.",
    "I see myself working in a technology-driven career.",
    "I want a role where I can influence strategic decisions.",
    "I prefer careers that involve continuous learning.",
    "I would enjoy a career that involves both technology and business.",
    "I see myself leading teams or organisations.",
    "I prefer careers that involve research or analysis.",
    "I want to work in fast-changing industries.",
    "I prefer careers involving problem-solving rather than routine tasks.",
    "I see myself contributing to technological or social transformation.",
    "I want to build innovative solutions rather than maintain old systems.",
  ];

  static String getSectionForQuestion(int index) {
    if (index < 10) return sections[0];
    if (index < 20) return sections[1];
    if (index < 30) return sections[2];
    return sections[3];
  }
}
