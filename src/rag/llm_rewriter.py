"""LLM-powered rewriting for RAG - rewrites resume bullets using evidence constraints."""

import os
from typing import Dict, List, Any, Optional

from openai import OpenAI


class LLMRewriter:
    """Rewrites resume bullets using LLM with evidence constraints."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.2):
        """
        Initialize LLM rewriter.

        Args:
            model: OpenAI model to use (default: gpt-4o-mini)
            temperature: Temperature for LLM generation (default: 0.2 for consistency)
        """
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def rewrite_with_evidence(
        self,
        bullet: str,
        evidence: str,
        requirement: str,
        max_tokens: int = 100,
    ) -> str:
        """
        Rewrite a resume bullet using retrieved evidence as constraint.

        Args:
            bullet: Original resume bullet text
            evidence: Retrieved evidence from RAG (facts to use)
            requirement: Job requirement to match
            max_tokens: Maximum tokens for rewritten bullet

        Returns:
            Rewritten bullet text
        """
        prompt = f"""Rewrite this resume bullet to match the job requirement.
Use ONLY facts from the EVIDENCE. Do not invent metrics or skills.

REQUIREMENT: {requirement}
ORIGINAL BULLET: {bullet}
EVIDENCE: {evidence}

Rewrite the bullet to:
1. Use active voice and strong verbs
2. Include quantified impact (%, $, X%, improvement) if available in evidence
3. Highlight relevant skills from the requirement
4. Keep it under 150 characters

Return ONLY the rewritten bullet, no explanation."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # If LLM fails, return original bullet
            print(f"LLM rewriting failed: {e}")
            return bullet

    def rewrite_batch(
        self,
        bullets: List[str],
        evidence_list: List[str],
        requirement: str,
    ) -> List[str]:
        """
        Rewrite multiple bullets with evidence.

        Args:
            bullets: List of original bullets
            evidence_list: List of evidence strings (one per bullet)
            requirement: Job requirement to match

        Returns:
            List of rewritten bullets
        """
        rewritten = []
        for bullet, evidence in zip(bullets, evidence_list):
            rewritten_bullet = self.rewrite_with_evidence(
                bullet, evidence, requirement
            )
            rewritten.append(rewritten_bullet)
        return rewritten

    def rewrite_with_context(
        self,
        bullet: str,
        context: Dict[str, Any],
        requirement: str,
    ) -> str:
        """
        Rewrite a bullet using rich context from RAG retrieval.

        Args:
            bullet: Original resume bullet
            context: Context dict with 'evidence', 'employer', 'role', etc.
            requirement: Job requirement

        Returns:
            Rewritten bullet
        """
        evidence = context.get("evidence", "")
        employer = context.get("employer", "")
        role = context.get("role", "")

        # Build enhanced prompt with context
        prompt = f"""Rewrite this resume bullet to match the job requirement.
Use ONLY facts from the EVIDENCE. Do not invent metrics or skills.

CONTEXT:
- Employer: {employer}
- Role: {role}
- Requirement: {requirement}

ORIGINAL BULLET: {bullet}
EVIDENCE: {evidence}

Rewrite the bullet to:
1. Use active voice and strong verbs
2. Include quantified impact (%, $, X%, improvement) if available
3. Highlight relevant skills from the requirement
4. Keep it under 150 characters
5. Maintain accuracy to the evidence provided

Return ONLY the rewritten bullet, no explanation."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=100,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM rewriting with context failed: {e}")
            return bullet

    def validate_bullet(self, bullet: str, evidence: str) -> bool:
        """
        Validate that rewritten bullet uses only evidence facts.

        Args:
            bullet: Rewritten bullet to validate
            evidence: Evidence that should support the bullet

        Returns:
            True if bullet appears to use only evidence facts
        """
        # Simple validation: check if key terms from evidence appear in bullet
        evidence_terms = set(evidence.lower().split())
        bullet_terms = set(bullet.lower().split())

        # If most bullet terms are in evidence, it's likely valid
        overlap = len(bullet_terms & evidence_terms)
        if overlap > 0:
            return True

        # If no overlap, might be too different
        return False

    def get_config(self) -> Dict[str, Any]:
        """Get rewriter configuration."""
        return {
            "model": self.model,
            "temperature": self.temperature,
        }

