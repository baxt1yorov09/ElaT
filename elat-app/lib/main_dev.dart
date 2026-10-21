import 'bootstrap.dart';
import 'core/config/app_config.dart';

void main() {
  bootstrap(
    const AppConfig(
      flavor: Flavor.dev,
      apiBaseUrl: 'http://10.0.2.2:8000/api/v1',
      appName: 'Elat (dev)',
    ),
  );
}
