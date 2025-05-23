import type { FC, ReactNode } from 'react';

/**
 * Props for the FeatureCard component
 */
interface FeatureCardProps {
  /** Title of the feature card */
  title: string;
  /** Description of the feature */
  description: string;
  /** Text for the action button */
  actionText: string;
  /** Click handler for the action button */
  onActionClick?: () => void;
  /** Optional icon to display */
  icon?: ReactNode;
}

/**
 * FeatureCard component for displaying a feature with title, description and action
 * Used on the home page to showcase main features of the application
 */
const FeatureCard: FC<FeatureCardProps> = ({ 
  title, 
  description, 
  actionText, 
  onActionClick,
  icon 
}) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
      {icon && <div className="mb-4">{icon}</div>}
      
      <h2 className="text-xl font-semibold text-primary mb-3">{title}</h2>
      
      <p className="text-textSecondary mb-4">
        {description}
      </p>
      
      <button 
        className="text-primary font-medium hover:underline"
        onClick={onActionClick}
      >
        {actionText}
      </button>
    </div>
  );
};

export default FeatureCard;
