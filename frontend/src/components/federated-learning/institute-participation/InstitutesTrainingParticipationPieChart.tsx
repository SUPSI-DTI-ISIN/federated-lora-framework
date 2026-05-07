import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip,
    Legend,
} from "recharts";
import type { InstituteTrainingParticipationDTO } from "@isin/institute-service-client";

interface InstitutesTrainingParticipationPieChartProps {
    institutesTrainingParticipation: InstituteTrainingParticipationDTO[];
}

const COLORS = [
    "#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd",
    "#06b6d4", "#22c55e", "#84cc16", "#eab308",
    "#f97316", "#ef4444", "#ec4899", "#14b8a6"
];

export const InstitutesTrainingParticipationPieChart = ({
                                                            institutesTrainingParticipation,
                                                        }: InstitutesTrainingParticipationPieChartProps) => {

    const data = institutesTrainingParticipation
        .filter((inst) => inst.trainable_samples_number && inst.trainable_samples_number > 0)
        .map((inst) => ({
            name: inst.institute_name,
            value: inst.is_reachable ? inst.trainable_samples_number ?? 0 : 0,
            is_reachable: inst.is_reachable,
        }));

    return (
        <div className="w-full h-[400px]">
            <ResponsiveContainer>
                <PieChart>
                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        outerRadius={140}
                        innerRadius={50}
                        paddingAngle={2}
                    >
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={
                                    entry.is_reachable
                                        ? COLORS[index % COLORS.length]
                                        : "#cbd5e1" // grey for unreachable
                                }
                                opacity={entry.is_reachable ? 1 : 0.6}
                            />
                        ))}
                    </Pie>

                    <Tooltip />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};