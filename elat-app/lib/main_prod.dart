import 'bootstrap.dart';
import 'core/config/app_config.dart';

void main() {
  bootstrap(
    const AppConfig(
      flavor: Flavor.prod,
      apiBaseUrl: 'https://api.elat.uz/api/v1',
      appName: 'Elat',
    ),
  );
}
