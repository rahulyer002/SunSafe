export function getRiskLevel(uvIndex) {
  if (uvIndex === 0) return "Minimal";
  if (uvIndex <= 2) return "Low";
  if (uvIndex <= 5) return "Moderate";
  if (uvIndex <= 7) return "High";
  if (uvIndex <= 10) return "Very High";
  return "Extreme";
}

export function getRiskColorClass(riskLevel) {
  if (riskLevel === "Low") return "uv-low";
  if (riskLevel === "Moderate") return "uv-moderate";
  if (riskLevel === "High") return "uv-high";
  if (riskLevel === "Very High") return "uv-very-high";
  if (riskLevel === "Extreme") return "uv-extreme";
  if (riskLevel === "Minimal") return "uv-minimal";
  return "";
}

export function getEstimatedBurnTime(uvIndex) {
  if (uvIndex <= 2) return "more than 60 minutes";
  if (uvIndex <= 5) return "about 45 minutes";
  if (uvIndex <= 7) return "about 25 minutes";
  if (uvIndex <= 10) return "about 15 minutes";
  return "less than 10 minutes";
}

export function getProtectionAdvice(uvIndex) {
  if (uvIndex === null || uvIndex === undefined) {
    return "UV data is not available right now.";
  }
  const burnTime = getEstimatedBurnTime(uvIndex);

  if (uvIndex === 0) {
    return `Your skin is at minimal risk, but it's always good to be cautious when spending extended time outdoors.`;
  }

  if (uvIndex <= 2) {
    return `Your skin is at low risk, but sun protection is still recommended for long outdoor exposure.`;
  }

  if (uvIndex <= 5) {
    return `Your skin may begin burning in ${burnTime}. Apply sunscreen and stay aware of sun exposure.`;
  }

  if (uvIndex <= 7) {
    return `Your skin may begin burning in ${burnTime}. Seek shade and wear protective clothing.`;
  }

  if (uvIndex <= 10) {
    return `Your skin may begin burning in ${burnTime}. Limit direct sun exposure and protect your skin now.`;
  }

  return `Your skin may begin burning in ${burnTime}. Avoid direct sunlight and take immediate protective action.`;
}
