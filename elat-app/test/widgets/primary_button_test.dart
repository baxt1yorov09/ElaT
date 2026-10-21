import 'package:elat/shared/widgets/primary_button.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../helpers.dart';

void main() {
  testWidgets('shows label and fires onPressed', (tester) async {
    var tapped = 0;
    await tester.pumpWidget(
      wrap(PrimaryButton(label: 'Qo\'llash', onPressed: () => tapped++)),
    );
    expect(find.text('Qo\'llash'), findsOneWidget);
    await tester.tap(find.byType(PrimaryButton));
    expect(tapped, 1);
  });

  testWidgets('loading hides label and disables tap', (tester) async {
    var tapped = 0;
    await tester.pumpWidget(
      wrap(PrimaryButton(label: 'X', loading: true, onPressed: () => tapped++)),
    );
    expect(find.text('X'), findsNothing);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    await tester.tap(find.byType(PrimaryButton));
    expect(tapped, 0);
  });
}
