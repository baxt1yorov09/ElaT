import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_theme.dart';
import '../../../core/theme/colors.dart';
import '../../../core/theme/spacing.dart';
import '../../../l10n/generated/app_localizations.dart';
import '../../../shared/widgets/centered_body.dart';
import '../../../shared/widgets/listing_card.dart';
import '../../../shared/widgets/section_chip.dart';

/// Phase 0 placeholder home. Real home (nearby row, TOP grid, ads) lands in Phase 1.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final sections = context.sections;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
        actions: [
          IconButton(
            tooltip: l10n.galleryTitle,
            onPressed: () => context.go('/home/gallery'),
            icon: const Icon(Icons.widgets_outlined),
          ),
        ],
      ),
      body: CenteredBody(
        child: ListView(
          padding: const EdgeInsets.all(Spacing.screen),
          children: [
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  SectionChip(
                    label: l10n.sectionAll,
                    // "Hammasi" is a neutral filter, not a section: use the
                    // brand accent (Coral), never a section color.
                    color: ElatColors.coral,
                    selected: true,
                  ),
                  const SizedBox(width: Spacing.s8),
                  SectionChip(
                    label: l10n.sectionSaxovat,
                    color: sections.saxovat,
                    selected: false,
                  ),
                  const SizedBox(width: Spacing.s8),
                  SectionChip(
                    label: l10n.sectionSavdo,
                    color: sections.savdo,
                    selected: false,
                  ),
                  const SizedBox(width: Spacing.s8),
                  SectionChip(
                    label: l10n.sectionBaraholka,
                    color: sections.baraholka,
                    selected: false,
                  ),
                ],
              ),
            ),
            const SizedBox(height: Spacing.s16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: Spacing.s12,
              crossAxisSpacing: Spacing.s12,
              childAspectRatio: 0.72,
              children: const [
                ListingCard(
                  data: ListingCardData(
                    title: 'Bolalar aravachasi',
                    location: 'Chilonzor',
                    timeAgo: '2 soat',
                    isFree: true,
                  ),
                ),
                ListingCard(
                  data: ListingCardData(
                    title: 'iPhone 12, yaxshi holatda',
                    location: 'Yunusobod',
                    timeAgo: '5 soat',
                    priceLabel: '4 200 000 so\'m',
                    isTop: true,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
