from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class DataClassificationTagRule(CloudFormationLintRule):
    """Check Resources have DataClassification Tag"""
    id = 'E9000'  # custom rule IDs start at 9000
    shortdesc = 'Resource has DataClassification Tag'
    description = 'Check that resources have a DataClassification tag'
    tags = ['resources', 'tags']

    def match(self, cfn):
        """Check resources have DataClassification tag"""
        matches = []
        resources = cfn.get_resources()

        for resource_name, resource_values in resources.items():
            resource_type = resource_values.get('Type', '')
            
            # Skip non-taggable resources
            if not self._is_taggable_resource(resource_type):
                continue
                
            properties = resource_values.get('Properties', {})
            tags = properties.get('Tags', [])
            
            # Handle direct tag lists
            if isinstance(tags, list):
                has_data_classification = False
                for tag in tags:
                    if isinstance(tag, dict) and tag.get('Key') == 'DataClassification':
                        has_data_classification = True
                        break
                
                if not has_data_classification:
                    message = f'Resource {resource_name} does not have required DataClassification tag'
                    path = ['Resources', resource_name, 'Properties', 'Tags']
                    matches.append(RuleMatch(path, message))
        
        return matches
    
    def _is_taggable_resource(self, resource_type):
        """Check if a resource type supports tagging"""
        taggable_resource_prefixes = [
            'AWS::S3::',
            'AWS::Redshift::Cluster',
            'AWS::RDS::'
        ]
        
        # Check if resource type starts with any taggable prefix
        for prefix in taggable_resource_prefixes:
            if resource_type.startswith(prefix):
                return True
                
        return False
