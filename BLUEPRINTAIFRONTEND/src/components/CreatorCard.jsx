import { Link } from "react-router-dom";

export default function CreatorCard({ creator }) {
  const engagement =
    Number(creator.total_likes || 0) +
    Number(creator.total_comments || 0) +
    Number(creator.total_shares || 0);

  return (
    <Link
      to={`/creators/${creator.id}`}
      className="block rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
    >
      <div className="flex items-center gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 text-xl font-bold">
          {creator.profile_image ? (
            <img
              src={creator.profile_image}
              alt={creator.name}
              className="h-14 w-14 rounded-full object-cover"
            />
          ) : (
            creator.name?.charAt(0)?.toUpperCase() || "C"
          )}
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {creator.name}
          </h3>
          <p className="text-sm text-gray-500">@{creator.tiktok_handle}</p>
        </div>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-gray-500">Followers</p>
          <p className="font-semibold">
            {Number(creator.follower_count || 0).toLocaleString()}
          </p>
        </div>

        <div>
          <p className="text-gray-500">Videos</p>
          <p className="font-semibold">{creator.total_videos || 0}</p>
        </div>

        <div>
          <p className="text-gray-500">Views</p>
          <p className="font-semibold">
            {Number(creator.total_views || 0).toLocaleString()}
          </p>
        </div>

        <div>
          <p className="text-gray-500">Revenue</p>
          <p className="font-semibold">
            ${Number(creator.total_revenue || 0).toLocaleString()}
          </p>
        </div>

        <div>
          <p className="text-gray-500">Engagement</p>
          <p className="font-semibold">{engagement.toLocaleString()}</p>
        </div>

        <div>
          <p className="text-gray-500">Conversions</p>
          <p className="font-semibold">
            {Number(creator.total_conversions || 0).toLocaleString()}
          </p>
        </div>
      </div>
    </Link>
  );
}