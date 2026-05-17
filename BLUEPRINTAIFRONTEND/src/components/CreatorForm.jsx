import { useState } from "react";

export default function CreatorForm({
  onSubmit,
  initialData = {},
  submitLabel = "Save Creator",
}) {
  const [formData, setFormData] = useState({
    name: initialData.name || "",
    tiktok_handle: initialData.tiktok_handle || "",
    profile_image: initialData.profile_image || "",
    follower_count: initialData.follower_count || 0,
    category: initialData.category || "",
    notes: initialData.notes || "",
    total_videos: initialData.total_videos || 0,
    total_views: initialData.total_views || 0,
    total_likes: initialData.total_likes || 0,
    total_comments: initialData.total_comments || 0,
    total_shares: initialData.total_shares || 0,
    total_conversions: initialData.total_conversions || 0,
    total_revenue: initialData.total_revenue || 0,
  });

  function handleChange(event) {
    const { name, value, type } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: type === "number" ? Number(value) : value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(formData);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <div className="grid gap-4 md:grid-cols-2">
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Creator name"
          className="rounded-xl border border-gray-300 px-4 py-2"
          required
        />

        <input
          name="tiktok_handle"
          value={formData.tiktok_handle}
          onChange={handleChange}
          placeholder="TikTok handle"
          className="rounded-xl border border-gray-300 px-4 py-2"
          required
        />

        <input
          name="profile_image"
          value={formData.profile_image}
          onChange={handleChange}
          placeholder="Profile image URL"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          name="category"
          value={formData.category}
          onChange={handleChange}
          placeholder="Creator category"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="follower_count"
          value={formData.follower_count}
          onChange={handleChange}
          placeholder="Follower count"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_videos"
          value={formData.total_videos}
          onChange={handleChange}
          placeholder="Total videos"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_views"
          value={formData.total_views}
          onChange={handleChange}
          placeholder="Total views"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_likes"
          value={formData.total_likes}
          onChange={handleChange}
          placeholder="Total likes"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_comments"
          value={formData.total_comments}
          onChange={handleChange}
          placeholder="Total comments"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_shares"
          value={formData.total_shares}
          onChange={handleChange}
          placeholder="Total shares"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_conversions"
          value={formData.total_conversions}
          onChange={handleChange}
          placeholder="Total conversions"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />

        <input
          type="number"
          name="total_revenue"
          value={formData.total_revenue}
          onChange={handleChange}
          placeholder="Total revenue"
          className="rounded-xl border border-gray-300 px-4 py-2"
        />
      </div>

      <textarea
        name="notes"
        value={formData.notes}
        onChange={handleChange}
        placeholder="Creator notes"
        className="mt-4 min-h-24 w-full rounded-xl border border-gray-300 px-4 py-2"
      />

      <button
        type="submit"
        className="mt-4 rounded-xl bg-black px-5 py-2 font-medium text-white hover:bg-gray-800"
      >
        {submitLabel}
      </button>
    </form>
  );
}