import 'bootstrap.dart';
import 'core/config/app_config.dart';

void main() {
  bootstrap(
    const AppConfig(
      flavor: Flavor.staging,
      apiBaseUrl: 'https://staging.elat.uz/api/v1',
      appName: 'Elat (staging)',
    ),
  );
}
