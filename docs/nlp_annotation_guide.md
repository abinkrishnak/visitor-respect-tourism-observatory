# NLP Annotation Guide

## Purpose

This guide helps human reviewers consistently label tourism-related discussion.
A document may receive more than one theme.

Do not label a nationality, ethnicity, country, person, or group as good, bad,
respectful, disrespectful, or risky. Label the discussion theme only.

## Labels

| Label | Apply when the text discusses | Do not apply when |
|---|---|---|
| Crowding and access | Queues, congestion, access pressure, overcrowded public spaces, difficulty using shared facilities | It is only a general complaint with no tourism/place context |
| Visitor respect and etiquette | Observable behaviour in shared, cultural, religious, heritage, or public spaces | It attacks an identity/group without describing an observable situation |
| Environment and cleanliness | Litter, waste, damage to nature, pollution, public cleanliness, resource pressure | It is only a hotel-room or personal-service complaint |
| Cost and displacement | Tourism-linked price pressure, housing concerns, local displacement, unaffordable visitor areas | It is only a generic personal expense |
| Positive coexistence | Respectful behaviour, community benefit, constructive tourism management, positive visitor-local interaction | It is generic praise without tourism context |
| Unclear / no relevant theme | The text is ambiguous, irrelevant, too short, or contains no tourism-impact theme | A clear label is supported by the text |

## Multi-label rule

More than one label may be selected. For example, a post about visitors leaving
litter at an overcrowded attraction can receive:

- Crowding and access
- Environment and cleanliness
- Visitor respect and etiquette

## Decision rules

1. Read the full document before labelling.
2. Label only what is stated or clearly described.
3. Do not infer a writer's identity, location, nationality, or visitor status.
4. If unsure, select `Unclear / no relevant theme` and add a short note.
5. Do not use sentiment alone as a theme label.
6. Record labels independently before discussing disagreements with another
   reviewer.

## Quality plan

- Two people independently label at least 200 shared documents.
- Compare labels before resolving disagreements.
- Record agreement and revise unclear definitions before training a model.
- Keep a held-out test sample separate from model training and tuning.