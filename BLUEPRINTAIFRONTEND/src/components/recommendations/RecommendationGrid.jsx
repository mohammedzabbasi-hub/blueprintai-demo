import RecommendationCard from "./RecommendationCard";

export default function RecommendationGrid({ items = [] }) {
  if (!items.length) {
    return <div className="text-sm text-gray-600">No recommendations available yet.</div>;
  }

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
      {items.map((item) => (
        <RecommendationCard key={item.id ?? `${item.category}-${item.name}`} item={item} />
      ))}
    </div>
  );
}
