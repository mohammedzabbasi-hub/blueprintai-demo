function Section({ title, items = [] }) {
  return (
    <div className="mt-5">
      <h3 className="font-medium mb-2">{title}</h3>
      <div className="space-y-2">
        {items.length === 0 && <div className="text-sm text-gray-600">No data.</div>}
        {items.map((item, index) => (
          <div key={`${title}-${index}`} className="border rounded-xl p-3 text-sm">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ComparisonInsightsCard({ comparison }) {
  if (!comparison) return null;

  return (
    <div className="border rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-4">Comparison Output</h2>
      <Section title="Best Hooks" items={comparison.best_hooks} />
      <Section title="Best Creator Types" items={comparison.best_creator_types} />
      <Section title="Best Humor Styles" items={comparison.best_humor_styles} />
      <Section title="Best Delivery Styles" items={comparison.best_delivery_styles} />
      <Section title="Best Promoter Types" items={comparison.best_promoter_types} />
      <Section title="Patterns" items={comparison.patterns} />
      <Section title="Warnings" items={comparison.warnings} />
    </div>
  );
}
