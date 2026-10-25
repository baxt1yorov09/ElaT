import 'package:elat/core/theme/app_theme.dart';
import 'package:elat/core/theme/colors.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Coral primary has Navy foreground (never white)', () {
    final light = AppTheme.light();
    expect(light.colorScheme.primary, ElatColors.coral);
    expect(light.colorScheme.onPrimary, ElatColors.navy);
  });

  test('section color extension is attached in both themes', () {
    expect(AppTheme.light().extension<ElatSectionColors>(), isNotNull);
    expect(AppTheme.dark().extension<ElatSectionColors>(), isNotNull);
  });

  test('dark theme uses brighter Saxovat green', () {
    final dark = AppTheme.dark().extension<ElatSectionColors>()!;
    expect(dark.saxovat, ElatColors.saxovatDark);
  });
}
