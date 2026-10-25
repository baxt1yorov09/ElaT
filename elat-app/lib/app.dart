import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'core/config/app_config.dart';
import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';
import 'l10n/generated/app_localizations.dart';

class ElatApp extends StatefulWidget {
  const ElatApp({super.key});

  @override
  State<ElatApp> createState() => _ElatAppState();
}

class _ElatAppState extends State<ElatApp> {
  final _router = createRouter();

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: AppConfig.current.appName,
      debugShowCheckedModeBanner: !AppConfig.current.isProd,
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: ThemeMode.system,
      routerConfig: _router,
      // Default language is Uzbek (Latin). The device/browser language must
      // not auto-switch the UI (e.g. to Russian); a user-chosen locale from
      // settings will override this in Phase 1.
      locale: const Locale('uz'),
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
    );
  }
}
