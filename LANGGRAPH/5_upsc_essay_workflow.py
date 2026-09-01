from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import operator

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash')

#define schema for models o/p
class EvaluationSchema(BaseModel):
    feedback : str = Field(description="Detailed feedback for the essay")
    score : int = Field(description="Score out of 10",ge=0,le=10)


structured_model = model.with_structured_output(EvaluationSchema)
# essay = """Economic Growth Without Social Justice Is a Recipe for ImplosionIntroduction: The Paradox of the Glittering TowerIn a rapidly globalizing world, national progress is frequently measured through numerical benchmarks: Gross Domestic Product (GDP), stock market indices, and foreign direct investment inflows. However, an economy that builds glittering skyscrapers while ignoring the slums at their bases constructs its foundation on shifting sand. History demonstrates that whenever economic expansion becomes decoupled from the equitable distribution of resources, societal cohesion weakens. Growth without equity is not true development; it is merely an accumulation of capital that triggers structural collapse.The Dimensional Matrix of Growth vs. JusticeThe Historical CrucibleHistorical precedents show that ignoring social justice during economic booms inevitably leads to unrest. The Ancien Regime of 18th-century France experienced substantial merchant wealth expansion, yet institutionalized inequality sparked the French Revolution. Similarly, the unbridled capitalism of the Gilded Age in the United States forced state intervention through the Progressive Era to avert systemic rebellion. Economic momentum without an ethical safety valve consistently results in structural collapse.The Economic Friction: The Underconsumption TrapWhen wealth concentrates heavily in the top decile of a population, the broader base suffers from depressed purchasing power. High-income individuals have a lower marginal propensity to consume compared to lower-income segments. This disparity leads to a structural crisis of underconsumption, asset bubbles, and long-term stagnation. True economic resilience requires a robust middle class, which can only be sustained through fair wages, labor protections, and social security.The Social and Psychological FracturesExtreme inequality erodes social capital—the trust that binds a community together. When the marginalized perceive that the rules of the economic game are permanently rigged against them, crime rates rise, social alienation deepens, and radicalization finds fertile ground. The psychological toll of relative deprivation breeds generational resentment, turning demographic dividends into demographic disasters.The Political Vulnerability: The Rise of DemagogueryWhen economic growth fails to deliver public goods like healthcare, quality education, and upward mobility, institutional legitimacy suffers. This systemic vacuum allows populist demagogues to exploit grievances, scapegoat minorities, and weaken democratic checks and balances. The resulting political instability deters investment, creating a self-reinforcing cycle of decay.The Indian Constitutional ParadigmFor a developing nation like India, this dynamic is central to governance. The framers of the Indian Constitution anticipated this challenge:The Preamble: Explicitly prioritizes Justice—social, economic, and political ahead of Liberty and Equality.Directive Principles (Part IV): Article 38 instructs the State to secure a social order aimed at promoting welfare, while Article 39 demands that the ownership and control of material resources are distributed to serve the common good, preventing the concentration of wealth.The Warning: As Dr. B.R. Ambedkar warned in his final address to the Constituent Assembly on November 25, 1949: "On the 26th of January 1950, we are going to enter into a life of contradictions. In politics we will have equality and in social and economic life we will have inequality... We must remove this contradiction at the earliest possible moment or else those who suffer from inequality will blow up the structure of political democracy."Path Forward: Constructing a Just EquilibriumTo transform growth from an exclusionary force into a shared asset, policy architecture must pivot from aggregate maximization to structural equity:Investing in Human Capability: Shift public spending toward universal high-quality primary healthcare and skill-based public education. True justice begins with expanding foundational opportunities.Progressive Fiscal Architecture: Implement tax reforms that penalize rent-seeking behavior while funding social safety nets, like automated universal basic insurances and rural employment guarantees.Fostering Inclusive Infrastructure: Direct capital into rural economies, decentralized micro-enterprises, and sustainable agricultural technologies to support the sectors where the majority of the population earns their livelihood.Conclusion: The Symmetric Architecture of ProgressEconomic growth and social justice are not competing values; they are complementary pillars. Growth provides the material resources needed to fund social justice, while social justice ensures the stable, inclusive environment required to sustain growth.A nation that pursues growth without equity will eventually face internal instability. Real progress is measured not by how high the wealthiest citizens can climb, but by the minimum standard of dignity guaranteed to the most vulnerable. True sustainable development requires building an economy where prosperity is shared, creating a resilient structure capable of enduring future challenges."""
# prompt = f"Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {essay}"
# res = structured_model.invoke(prompt)
# print(res)


class UpscState(TypedDict):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int],operator.add]#reducer function
    avg_score : float


#fns

def evaluate_language(state: UpscState):

    prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10\n\n{state['essay']}'
    output = structured_model.invoke(prompt)

    return {'language_feedback': output.feedback, 'individual_scores': [output.score]}

def evaluate_analysis(state: UpscState):

    prompt = f'Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10\n\n{state['essay']}'
    output = structured_model.invoke(prompt)

    return {'analysis_feedback': output.feedback, 'individual_scores': [output.score]}

def evaluate_thought(state: UpscState):

    prompt = f'Evaluate the clarity of thought of the following essay and provide a feedback and assign a score out of 10 \n {state['essay']}'
    output = structured_model.invoke(prompt)

    return {'clarity_feedback': output.feedback, 'individual_scores': [output.score]}

def final_evaluation(state: UpscState):

    # summary feedback
    prompt = f'Based on the following feedbacks create a summarized feedback \n language feedback - {state["language_feedback"]} \n depth of analysis feedback - {state["analysis_feedback"]} \n clarity of thought feedback - {state["clarity_feedback"]}'
    overall_feedback = model.invoke(prompt).content

    # avg calculate
    avg_score = sum(state['individual_scores'])/len(state['individual_scores'])

    return {'overall_feedback': overall_feedback, 'avg_score': avg_score}


#graph
graph = StateGraph(UpscState)

graph.add_node('evaluate_language', evaluate_language)
graph.add_node('evaluate_analysis', evaluate_analysis)
graph.add_node('evaluate_thought', evaluate_thought)
graph.add_node('final_evaluation', final_evaluation)

# edges
graph.add_edge(START, 'evaluate_language')
graph.add_edge(START, 'evaluate_analysis')
graph.add_edge(START, 'evaluate_thought')

graph.add_edge('evaluate_language', 'final_evaluation')
graph.add_edge('evaluate_analysis', 'final_evaluation')
graph.add_edge('evaluate_thought', 'final_evaluation')

graph.add_edge('final_evaluation', END)

workflow = graph.compile()
#bad
essay ="""The modern paradigm of socio-economic development necessitates a multilateral approach towards the juxtaposition of institutional frameworks and grassroots mobilization. In this context, one must ponder whether the teleological suspension of the ethical is truly concomitant with the bureaucratic inertia plaguing our hinterlands. Therefore, bridging the ontological gap between policy formulation and implementation requires a panacea of multifaceted synergy, or perhaps, a paradigm shift that lacks logical coherence.The Duality of Dichotomies in PolityThe state is an apparatus of structural hegemony yet a harbinger of welfare economics simultaneously.Pertaining to the aforesaid, fiscal federalism often oscillates like a pendulum in a vacuum.Consequently, agrarian distress is not merely a localized phenomenon, but an epiphenomenon of globalized capitalism interacting with local feudal remnants.Institutional Apathy Versus Teleological AspirationsBureaucracy functions on red tape, which metaphorically strangles the umbilical cord of inclusive growth.Citizens feel alienated, much like a fish out of water in the Sahara desert of administrative red tape.It is imperative to realize that the lack of thought clarity is itself a profound reflection of the systemic chaos.Ultimately, the wheel of progress spins in circles, leading us back to the square one of theoretical ambiguity. Thus, the quintessence of governance remains an elusive chimera, dancing on the precipice of syntactic disorder and profound philosophical confusion."""
#good
#essay = """IntroductionThe trajectory of human civilization has always been steered by its primary technologies, from the steam engine to the internet. Today, Artificial Intelligence (AI) stands as the defining paradigm shift of the 21st century. Unlike previous tools that augmented physical muscle, AI augments cognitive capacity. This fundamental difference creates a profound civilizational paradox. AI possesses the potential to democratize knowledge and revolutionize human capability, yet it simultaneously threatens to concentrate power, automate bias, and widen global inequalities. The ultimate destination of this technological transition depends entirely on the governance frameworks we build today.AI as a Catalyst for Human EmpowermentDemocratization of Expertise: Historically, specialized knowledge—be it medical diagnostics, legal analysis, or advanced coding—was locked behind expensive institutional barriers. Generative AI and LLMs act as cognitive equalizers, giving a student in a remote village access to personalized elite tutoring, or a rural entrepreneur the tools to build software and navigate complex regulations without expensive consultants.Amplifying Public Goods: In critical sectors like healthcare and agriculture, AI functions as a force multiplier. Machine learning algorithms can predict crop failures, optimize water usage for smallholder farmers, and diagnose diseases from low-resolution medical images in regions lacking specialized doctors. It shifts the paradigm from reactive treatment to proactive intervention.Liberation from Drudgery: By automating repetitive analytical and administrative tasks, AI has the capacity to free human labor for higher-order creative, empathetic, and strategic endeavors, sparking a new renaissance of human-centric work.AI as an Engine of MarginalizationThe New Cognitive Divide: While the digital divide was about access to hardware and internet, the AI divide is about access to sophisticated cognitive infrastructure. Countries and corporations that own the compute, data pipelines, and foundational models will hold unprecedented asymmetric power, reducing the Global South to mere consumers and data exporters—a dynamic termed "data colonialism."Systemic Job Displacement: Previous industrial revolutions allowed labor to transition from farms to factories. The AI revolution moves at an exponential pace, threatening to displace cognitive and creative labor faster than social safety nets can adapt. This risks creating a massive, structurally unemployed "underclass" whose skills are permanently obsolete.Codified Inequities and Algorithmic Bias: AI systems are trained on historical data, which reflects historical human prejudices. When used in judicial sentencing, predatory lending, or resume screening, these algorithms do not eliminate human bias; they optimize, scale, and institutionalize it under the guise of "objective math," further marginalizing vulnerable communities.The Indian Imperative: AI for All (#AIforAll)For a developing nation like India, AI is a high-stakes arena. With a massive youth population, unbridled automation could disrupt the IT and services sector, which has been a primary engine of middle-class growth. Conversely, deploying localized AI tools in vernacular languages can bridge massive governance deficits in public administration, financial inclusion, and judicial pendency. India’s strategic stance must reject passive adoption and instead pioneer "frugal, inclusive AI" designed for social impact rather than corporate rent-seeking.The Path Forward: Frameworks for Inclusive AITo ensure that technology serves as a tool for empowerment rather than exclusion, global governance must shift from laissez-faire commercialism to ethical constitutionalism:Algorithmic Accountability: Governments must mandate strict, independent audits of high-stakes AI models to ensure transparency, explainability, and the eradication of data bias before deployment.Democratic Compute Infrastructure: Access to advanced compute must be treated as a modern public utility. Publicly funded AI research centers must be established to build open-source, localized models tailored for social welfare rather than advertising revenue.Re-skilling and Social Safety Safety Nets: As structural displacement occurs, fiscal policy must adapt. This includes exploring frameworks like data-dividend taxation to fund universal lifelong learning credits and robust social security buffers for transitioning workers.ConclusionArtificial Intelligence is neither inherently a savior nor a destroyer; it is a mirror reflecting the socio-economic priorities of its creators. If left entirely to market forces, AI will naturally concentrate capital and accelerate marginalization. However, if guided by the principles of social justice, equity, and human rights, it can become the most powerful equalizer in human history. The challenge ahead is not technical, but ethical—ensuring that as our machines become smarter, our societies become more just."""
initial_state = {
    'essay' : essay
}

res = workflow.invoke(initial_state)
print(res)
print("--- OVERALL FEEDBACK ---")
print(res['overall_feedback'])
print(f"\n--- AVERAGE SCORE: {res['avg_score']}/10 ---")
