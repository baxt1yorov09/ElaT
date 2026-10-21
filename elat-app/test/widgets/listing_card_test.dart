import 'package:elat/shared/widgets/listing_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../helpers.dart';

void main() {
  testWidgets('free listing shows BEPUL label, not a price', (tester) async {
    await tester.pumpWidget(
      wrap(
        const SizedBox(
          width: 200,
          height: 260,
          child: ListingCard(
            data: ListingCardData(
              title: 'Divan',
              location: 'Chilonzor',
              timeAgo: '1 soat',
              isFree: true,
            ),
          ),
        ),
      ),
    );
    expect(find.text('BEPUL'), findsOneWidget);
    expect(find.text('Divan'), findsOneWidget);
  });

  testWidgets('priced listing shows the price label', (tester) async {
    await tester.pumpWidget(
      wrap(
        const SizedBox(
          width: 360,
          child: ListingCard(
            layout: ListingCardLayout.list,
            data: ListingCardData(
              title: 'iPhone 12',
              location: 'Yunusobod',
              timeAgo: '2 soat',
              priceLabel: '4 200 000',
            ),
          ),
        ),
      ),
    );
    expect(find.text('4 200 000'), findsOneWidget);
  });
}
