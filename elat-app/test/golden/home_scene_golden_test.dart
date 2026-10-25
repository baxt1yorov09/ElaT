import 'package:elat/core/theme/app_theme.dart';
import 'package:elat/core/theme/colors.dart';
import 'package:elat/core/theme/spacing.dart';
import 'package:elat/shared/widgets/listing_card.dart';
import 'package:elat/shared/widgets/section_chip.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../helpers.dart';

/// A compact scene that locks the reviewed visuals: neutral "Hammasi" chip,
/// section chips, the free (BEPUL) card and a TOP card — in light and dark.
Widget _scene() {
  return Builder(
    builder: (context) {
      final sections = context.sections;
      return SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(Spacing.screen),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const SectionChip(
                    label: 'Hammasi',
                    color: ElatColors.coral,
                    selected: true,
                  ),
                  const SizedBox(width: Spacing.s8),
                  SectionChip(
                    label: 'Saxovat',
                    color: sections.saxovat,
                    selected: false,
                  ),
                ],
              ),
              const SizedBox(height: Spacing.s16),
              const SizedBox(
                width: 180,
                height: 265,
                child: ListingCard(
                  data: ListingCardData(
                    title: 'Divan, yaxshi holatda',
                    location: 'Chilonzor',
                    timeAgo: '1 soat',
                    isFree: true,
                  ),
                ),
              ),
              const SizedBox(height: Spacing.s12),
              const SizedBox(
                width: 340,
                height: 104,
                child: ListingCard(
                  layout: ListingCardLayout.list,
                  data: ListingCardData(
                    title: 'Velosiped',
                    location: 'Sergeli',
                    timeAgo: '3 soat',
                    priceLabel: '850 000',
                    isTop: true,
                  ),
                ),
              ),
            ],
          ),
        ),
      );
    },
  );
}

void main() {
  testWidgets('home scene golden — light', (tester) async {
    await tester.pumpWidget(wrap(_scene()));
    await tester.pumpAndSettle();
    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/home_scene_light.png'),
    );
  });

  testWidgets('home scene golden — dark', (tester) async {
    await tester.pumpWidget(wrap(_scene(), brightness: Brightness.dark));
    await tester.pumpAndSettle();
    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/home_scene_dark.png'),
    );
  });
}
