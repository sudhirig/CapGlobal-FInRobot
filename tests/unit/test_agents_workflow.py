"""
Unit tests for agent workflow and agent library
Tests agent initialization, workflows, and interactions
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.agents.workflow import SingleAssistant, MultiAssistant, MultiAssistantWithLeader
from finrobot.agents.agent_library import library
from tests.utils.test_helpers import TestHelpers


class TestAgentWorkflow:
    """Comprehensive tests for agent workflows"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_keys):
        """Setup for each test"""
        self.helpers = TestHelpers()
        
        if 'OPENAI_API_KEY' not in api_keys:
            pytest.skip("OPENAI_API_KEY not available")
        
        self.llm_config = {
            "config_list": [{
                "model": "gpt-4o",
                "api_key": api_keys['OPENAI_API_KEY']
            }],
            "temperature": 0.7,
            "timeout": 120,
        }
    
    def test_single_assistant_initialization(self):
        """Test SingleAssistant initialization"""
        assistant = SingleAssistant(
            "Test_Assistant",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3
        )
        
        assert assistant is not None, "Assistant should be initialized"
        assert assistant.assistant is not None, "Assistant agent should exist"
        assert assistant.user_proxy is not None, "User proxy should exist"
    
    def test_agent_library_has_agents(self):
        """Test that agent library contains agents"""
        assert library is not None, "Library should exist"
        assert len(library) > 0, "Library should have agents"
        
        # Verify agents have required structure
        for agent_name, agent_config in library.items():
            assert 'name' in agent_config, f"Agent {agent_name} should have name"
            assert 'profile' in agent_config or 'description' in agent_config, \
                f"Agent {agent_name} should have profile/description"
    
    def test_no_mock_agents(self):
        """Test that agents are not mock/test agents"""
        for agent_name, agent_config in library.items():
            # Check agent name
            assert not self.helpers.is_mock_data(agent_name), \
                f"Agent name contains mock data: {agent_name}"
            
            # Check agent config
            assert not self.helpers.is_mock_data(agent_config), \
                f"Agent config contains mock data: {agent_name}"

