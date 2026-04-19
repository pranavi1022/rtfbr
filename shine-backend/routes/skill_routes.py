"""
routes/skill_routes.py
Endpoint: POST /api/skill-gap
"""

from flask import Blueprint, request, jsonify
from logic.skill_engine import analyze_skill_gap

skill_bp = Blueprint('skill', __name__)


@skill_bp.route('/api/skill-gap', methods=['POST'])
def skill_gap():
    data = request.get_json() or {}

    project_description = data.get('projectName',  '').strip()
    project_type        = data.get('projectType',  'website').strip()
    user_skills         = data.get('skills',        [])

    if not project_description:
        return jsonify({"error": "projectName is required"}), 400

    if not user_skills or not isinstance(user_skills, list):
        return jsonify({"error": "At least one skill is required"}), 400

    # Normalise project type
    if project_type.lower() not in ('website', 'app', 'other'):
        project_type = 'website'

    result = analyze_skill_gap(project_description, project_type, user_skills)
    return jsonify(result), 200
