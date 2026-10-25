import 'package:elat/core/theme/colors.dart';
import 'package:elat/shared/widgets/app_badge.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../helpers.dart';

void main() {
  testWidgets('free badge is green with white text', (tester) async {
    await tester.pumpWidget(
      wrap(const AppBadge(label: 'BEPUL', kind: BadgeKind.free)),
    );
    expect(find.text('BEPUL'), findsOneWidget);
    final container = tester.widget<Container>(find.byType(Container));
    final decoration = container.decoration! as BoxDecoration;
    expect(decoration.color, ElatColors.saxovat);
  });

  testWidgets('top badge is Coral with Navy text (brand rule)', (tester) async {
    await tester.pumpWidget(
      wrap(const AppBadge(label: 'TOP', kind: BadgeKind.top)),
    );
    final text = tester.widget<Text>(find.text('TOP'));
    expect(text.style!.color, ElatColors.navy);
  });
}
