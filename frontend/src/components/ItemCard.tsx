import { Link } from "react-router-dom";
import type { ItemSummary } from "../types";

interface Props {
  item: ItemSummary;
}

export default function ItemCard({ item }: Props) {
  return (
    <Link
      to={`/${item.category}/${item.id}`}
      className="item-card"
    >
      <h3 className="item-card-title">{item.title}</h3>
      <p className="item-card-desc">{item.short_description}</p>
      <div className="item-card-tags">
        {item.tags.map((tag) => (
          <span key={tag} className="tag">
            {tag}
          </span>
        ))}
      </div>
    </Link>
  );
}
