import 'package:flutter/material.dart';

import '../../core/theme/app_theme.dart';
import '../../core/theme/spacing.dart';
import '../../l10n/generated/app_localizations.dart';
import '../../shared/widgets/app_badge.dart';
import '../../shared/widgets/app_snackbar.dart';
import '../../shared/widgets/app_text_field.dart';
import '../../shared/widgets/centered_body.dart';
import '../../shared/widgets/empty_state.dart';
import '../../shared/widgets/listing_card.dart';
import '../../shared/widgets/primary_button.dart';
import '../../shared/widgets/secondary_button.dart';
import '../../shared/widgets/section_chip.dart';
import '../../shared/widgets/skeleton_box.dart';

/// Phase 0 component gallery. Verifies tokens and shared widgets in light + dark.
class GalleryScreen extends StatelessWidget {
  const GalleryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final sections = context.sections;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.galleryTitle)),
      body: CenteredBody(
        child: ListView(
          padding: const EdgeInsets.all(Spacing.screen),
          children: [
            _section('Buttons'),
            PrimaryButton(
              label: l10n.actionApply,
              icon: Icons.check,
              onPressed: () => showAppSnackbar(
                context,
                message: l10n.actionApply,
                kind: SnackKind.success,
              ),
            ),
            const SizedBox(height: Spacing.s8),
            const PrimaryButton(
                label: 'Loading', loading: true, onPressed: null),
            const SizedBox(height: Spacing.s8),
            SecondaryButton(
              label: l10n.actionClear,
              icon: Icons.close,
              onPressed: () {},
            ),
            const SizedBox(height: Spacing.s24),
            _section('Section chips'),
            Wrap(
              spacing: Spacing.s8,
              runSpacing: Spacing.s8,
              children: [
                SectionChip(
                  label: l10n.sectionSaxovat,
                  color: sections.saxovat,
                  selected: true,
                ),
                SectionChip(
                  label: l10n.sectionSavdo,
                  color: sections.savdo,
                  selected: false,
                ),
                SectionChip(
                  label: l10n.sectionBaraholka,
                  color: sections.baraholka,
                  selected: false,
                ),
                SectionChip(
                  label: l10n.sectionSwap,
                  color: sections.swap,
                  selected: false,
                ),
              ],
            ),
            const SizedBox(height: Spacing.s24),
            _section('Badges'),
            Wrap(
              spacing: Spacing.s8,
              children: [
                AppBadge(label: l10n.labelFree, kind: BadgeKind.free),
                AppBadge(label: l10n.labelTop, kind: BadgeKind.top),
                AppBadge(label: l10n.labelVerified, kind: BadgeKind.verified),
                const AppBadge(label: 'Auksion', kind: BadgeKind.auction),
              ],
            ),
            const SizedBox(height: Spacing.s24),
            _section('Text field'),
            AppTextField(label: l10n.navSearch, hint: '...'),
            const SizedBox(height: Spacing.s24),
            _section('Listing cards'),
            SizedBox(
              height: 230,
              child: GridView.count(
                crossAxisCount: 2,
                mainAxisSpacing: Spacing.s12,
                crossAxisSpacing: Spacing.s12,
                childAspectRatio: 0.72,
                children: [
                  ListingCard(
                    freeLabel: l10n.labelFree,
                    data: const ListingCardData(
                      title: 'Divan, yaxshi holatda',
                      location: 'Chilonzor',
                      timeAgo: '1 soat',
                      isFree: true,
                    ),
                  ),
                  ListingCard(
                    topLabel: l10n.labelTop,
                    data: const ListingCardData(
                      title: 'Velosiped',
                      location: 'Sergeli',
                      timeAgo: '3 soat',
                      priceLabel: '850 000 so\'m',
                      isTop: true,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: Spacing.s12),
            ListingCard(
              layout: ListingCardLayout.list,
              freeLabel: l10n.labelFree,
              data: const ListingCardData(
                title: 'Kitoblar to\'plami',
                location: 'Yakkasaroy',
                timeAgo: '10 daqiqa',
                isFree: true,
              ),
            ),
            const SizedBox(height: Spacing.s24),
            _section('Skeleton'),
            const SkeletonBox(height: 16, width: 180),
            const SizedBox(height: Spacing.s8),
            const SkeletonBox(height: 16, width: 120),
            const SizedBox(height: Spacing.s24),
            _section('Empty state'),
            SizedBox(
              height: 220,
              child: EmptyState(
                icon: Icons.inbox_outlined,
                title: l10n.emptyTitle,
                description: l10n.emptyDescription,
                action: SecondaryButton(
                  label: l10n.actionRetry,
                  onPressed: () {},
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _section(String title) => Padding(
        padding: const EdgeInsets.only(bottom: Spacing.s12),
        child: Text(
          title,
          style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 18),
        ),
      );
}
