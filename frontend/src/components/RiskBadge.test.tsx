import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import RiskBadge from "./RiskBadge";

describe("RiskBadge", () => {
  it("renders the transparent score and label", () => {
    render(<RiskBadge score={72} label="High" />);

    expect(screen.getByText("High")).toBeInTheDocument();
    expect(screen.getByText("72/100")).toBeInTheDocument();
  });
});

