import { ReactNode } from "react";

type SectionProps = {
  title: string;
  description?: string;
  children: ReactNode;
};

export function Section({ title, description, children }: SectionProps) {
  return (
    <section className="card">
      <h2>{title}</h2>
      {description && <p>{description}</p>}
      {children}
    </section>
  );
}
