<script setup>
import { ref } from "vue";

const query = ref("");
const showDiagram = ref(false);
const loading = ref(false);
const error = ref("");

// Example prompts
const examplePrompts = ref([
  "Rank these three compounds for EGFR inhibition: - Compound A: CC(C)Cc1ccc(cc1)C(C)C(O)=O - Compound B: CN1C=NC2=C1C(=O)N(C(=O)N2C)C - Compound C: CC(C)NCC(COc1ccccc1)O",
  "What would be the best starting point for lead optimization: aspirin (CC(=O)Oc1ccccc1C(=O)O) or ibuprofen (CC(C)Cc1ccc(cc1)C(C)C(O)=O)?",
  "What is Lipinski's rule of five?",
  "Compare the drug-likeness of caffeine (CN1C=NC2=C1C(=O)N(C(=O)N2C)C) and ethanol (CCO)",
]);

// API response data
const decision = ref(null);
const rationale = ref("");
const result = ref([]);
const toolResults = ref([]);

const playQuery = async () => {
  if (!query.value.trim()) return;

  loading.value = true;
  error.value = "";
  showDiagram.value = true;

  try {
    const response = await fetch("/api/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: query.value.trim(),
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Map the API response to reactive refs
    decision.value = data.decision;
    rationale.value = data.response?.rationale || "";
    result.value = data.response?.result || [];
    toolResults.value = data.tool_results || [];
  } catch (err) {
    error.value = err.message || "Failed to fetch data";
    console.error("API call failed:", err);
  } finally {
    loading.value = false;
  }
};

const selectExamplePrompt = (prompt) => {
  query.value = prompt;
  playQuery();
};
</script>

<template>
  <div class="app">
    <!-- Input Section -->
    <div class="input-section">
      <h1>Bio Context Enrichment</h1>

      <!-- Example Prompts Section -->
      <div class="example-prompts">
        <h3>Try these examples:</h3>
        <div class="examples-grid">
          <div
            v-for="(prompt, index) in examplePrompts"
            :key="index"
            class="example-prompt"
            @click="selectExamplePrompt(prompt)"
          >
            {{ prompt }}
          </div>
        </div>
      </div>

      <div class="input-group">
        <input
          v-model="query"
          type="text"
          placeholder="Enter your biological query..."
          class="query-input"
          @keyup.enter="playQuery"
        />
        <button
          @click="playQuery"
          class="play-button"
          :disabled="!query.trim() || loading"
        >
          {{ loading ? "Processing..." : "Prompt" }}
        </button>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error-message">
      <h3>Error</h3>
      <p>{{ error }}</p>
    </div>

    <!-- Diagram Section -->
    <div v-if="showDiagram && !error && !loading" class="diagram">
      <!-- Step 1: Query Understanding -->
      <div class="step">
        <div class="step-box">
          <h3>Step 1: Query Understanding</h3>
          <p>(Classification + Entity Extraction)</p>
          <div v-if="loading" class="loading">Loading...</div>
          <div v-else-if="decision" class="output">
            <div><strong>Action:</strong> {{ decision.action }}</div>
            <div v-if="decision.entities">
              <div v-if="decision.entities.compounds" class="compounds">
                <h4>Compounds:</h4>
                <ul>
                  <li
                    v-for="compound in decision.entities.compounds"
                    :key="compound.name"
                  >
                    <strong>{{ compound.name }}:</strong> {{ compound.smiles }}
                  </li>
                </ul>
              </div>
              <div v-if="decision.entities.target">
                <strong>Target:</strong> {{ decision.entities.target }}
              </div>
            </div>
            <div v-if="decision.needs_tools">
              <strong>Needs Tools:</strong>
              {{ decision.needs_tools ? "Yes" : "No" }}
            </div>
            <strong>Required Tools:</strong>
            <div>
              <ul>
                <li
                  v-for="tool in decision.required_tools"
                  :key="JSON.stringify(tool)"
                >
                  {{ tool }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="arrow">↓</div>
      </div>

      <!-- Step 2: Tool Results -->
      <div v-if="toolResults.length > 0" class="step">
        <div class="step-box">
          <h3>Step 2: Context Enrichment</h3>
          <p>(MCP tool calls)</p>
          <div class="tool-results">
            <div
              v-for="toolResult in toolResults"
              :key="toolResult.args.smiles"
              class="tool-result"
            >
              <h4>{{ toolResult.tool_name }}</h4>
              <div><strong>SMILES:</strong> {{ toolResult.args.smiles }}</div>
              <div><strong>Target:</strong> {{ toolResult.args.target }}</div>
              <div>
                <strong>Tool result:</strong>
                {{ toolResult.result }}
              </div>
            </div>
          </div>
        </div>
        <div class="arrow">↓</div>
      </div>

      <div v-if="toolResults.length == 0" class="step" disabled>
        <div class="step-box">
          <h3>Step 2: Context Enrichment</h3>
          <div>Skipping.</div>
        </div>
        <div class="arrow">↓</div>
      </div>

      <!-- Step 3: Final Result -->
      <div v-if="rationale || result.length > 0" class="step">
        <div class="step-box">
          <h3>Step 3: Final Result</h3>
          <p>(Reasoning)</p>
          <div v-if="rationale" class="output">
            <strong>Rationale:</strong>
            <p>{{ rationale }}</p>
          </div>
          <div v-if="result" class="output">
            <strong>Result:</strong>
            <p>{{ result }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.input-section {
  text-align: center;
  margin-bottom: 40px;
}

.input-section h1 {
  color: #333;
  margin-bottom: 20px;
}

.example-prompts {
  margin: 30px 0;
  text-align: center;
}

.example-prompts h3 {
  color: #555;
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: 500;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 12px;
  margin-bottom: 30px;
}

.example-prompt {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  line-height: 1.4;
  text-align: left;
  color: #495057;
  min-height: 60px;
  display: flex;
  align-items: center;
}

.example-prompt:hover {
  background: linear-gradient(135deg, #007acc 0%, #005a9e 100%);
  border-color: #004085;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 122, 204, 0.3);
}

.example-prompt:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 122, 204, 0.2);
}

.input-group {
  display: flex;
  gap: 10px;
  justify-content: center;
  align-items: center;
}

.query-input {
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  min-width: 300px;
  outline: none;
  transition: border-color 0.3s;
}

.query-input:focus {
  border-color: #007acc;
}

.play-button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.play-button:hover:not(:disabled) {
  background-color: #005a9e;
}

.play-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.diagram {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.step-box {
  background: #f8f9fa;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 400px;
  text-align: left;
}

.step-box h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
}

.step-box p {
  margin: 5px 0;
  color: #666;
  font-style: italic;
}

.step-box ul {
  margin: 10px 0;
  padding-left: 20px;
}

.step-box li {
  margin: 5px 0;
  color: #555;
}

.output {
  margin-top: 15px;
  padding: 10px;
  background: #fff;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.error-message {
  background: #fee;
  border: 1px solid #faa;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  color: #c00;
  text-align: center;
}

.loading {
  padding: 20px;
  text-align: center;
  font-style: italic;
  color: #666;
}

.compounds ul {
  margin: 5px 0;
  padding-left: 20px;
}

.compounds li {
  margin: 5px 0;
  word-break: break-all;
}

.tool-results {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tool-result {
  background: #f0f8ff;
  border: 1px solid #b6d7ff;
  border-radius: 6px;
  padding: 12px;
}

.tool-result h4 {
  margin: 0 0 8px 0;
  color: #0066cc;
  text-transform: capitalize;
}

.ranking {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 10px;
}

.ranking-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
}

.rank-number {
  background: #007acc;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.compound-info {
  flex: 1;
}

.compound-info h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.score {
  font-weight: bold;
  color: #007acc;
  margin-bottom: 5px;
}

.reason {
  color: #666;
  font-size: 14px;
}

.input-output {
  margin-top: 10px;
}

.arrow {
  font-size: 24px;
  color: #333;
  margin: 10px 0;
}

.annotations {
  position: absolute;
  right: -150px;
  top: 0;
  display: flex;
  flex-direction: column;
  gap: 100px;
}

.annotation {
  color: #666;
  font-size: 14px;
  font-style: italic;
}

.annotation.haiku {
  margin-top: 50px;
}

.annotation.no-llm {
  margin-top: 20px;
}

.annotation.sonnet {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .input-group {
    flex-direction: column;
  }

  .query-input {
    min-width: 250px;
  }

  .examples-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .example-prompt {
    min-height: 50px;
    font-size: 13px;
    padding: 10px 12px;
  }

  .annotations {
    display: none;
  }
}
</style>
