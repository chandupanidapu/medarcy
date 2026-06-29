import {
  Activity,
  Bell,
  BookOpenCheck,
  BrainCircuit,
  Circle,
  UserCircle2,
} from "lucide-react";

const systemStatus = {
  aiPipeline: "Operational",
  evidenceEngine: "Active",
  knowledgeBase: "Updated",
};

function StatusItem({ icon: Icon, title, value }) {
  return (
    <div className="status-item">
      <Icon size={16} className="status-icon" />

      <div className="status-text">
        <span className="status-title">{title}</span>
        <span className="status-value">
          <Circle
            size={8}
            fill="#22c55e"
            color="#22c55e"
          />
          {value}
        </span>
      </div>
    </div>
  );
}

function Header() {
  return (
    <header className="header">

      <div className="header-left">

        <h1>Clinical Intelligence Workspace</h1>

        <p>
          Evidence synthesis • Differential diagnosis • Medical research •
          Clinical decision support
        </p>

      </div>

      <div className="header-right">

        <StatusItem
          icon={BrainCircuit}
          title="AI Pipeline"
          value={systemStatus.aiPipeline}
        />

        <StatusItem
          icon={BookOpenCheck}
          title="Evidence Engine"
          value={systemStatus.evidenceEngine}
        />

        <StatusItem
          icon={Activity}
          title="Knowledge Base"
          value={systemStatus.knowledgeBase}
        />

        <div className="header-divider" />

        <button className="icon-button">
          <Bell size={18} />
        </button>

        <button className="icon-button">
          <UserCircle2 size={22} />
        </button>

      </div>

    </header>
  );
}

export default Header;