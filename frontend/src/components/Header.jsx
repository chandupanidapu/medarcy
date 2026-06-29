import {
  ShieldCheck,
  Activity,
  BrainCircuit,
} from "lucide-react";

function Header() {
  return (
    <header className="header">

      <div className="header-left">

        <h1>
          Clinical Workspace
        </h1>

        <p>
          AI-assisted evidence-based clinical decision support
        </p>

      </div>

      <div className="header-right">

        <div className="header-chip">
          <ShieldCheck size={16} />
          Clinical Mode
        </div>

        <div className="header-chip">
          <BrainCircuit size={16} />
          Gemini
        </div>

        <div className="header-chip">
          <Activity size={16} />
          Ready
        </div>

      </div>

    </header>
  );
}

export default Header;