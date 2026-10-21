/// Build flavor configuration (dev / staging / prod). Set from main_<flavor>.dart.
enum Flavor { dev, staging, prod }

class AppConfig {
  const AppConfig({
    required this.flavor,
    required this.apiBaseUrl,
    required this.appName,
  });

  final Flavor flavor;
  final String apiBaseUrl;
  final String appName;

  bool get isProd => flavor == Flavor.prod;

  static late AppConfig current;

  static void init(AppConfig config) => current = config;
}
